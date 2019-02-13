import copy
import logging
from collections import OrderedDict as OD

from django.db import transaction


from glamod.parser.settings import *
from glamod.parser.utils import timeit
from glamod.parser.chunk_manager import ChunkManager
from glamod.parser.exceptions import ParserError

from glamod.parser.rules import (SourceConfigurationParserRules,
    StationConfigurationParserRules, StationConfigurationOptionalParserRules,
    HeaderTableParserRules, ObservationsTableParserRules)
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class _DBWriterBase(object):

    app_model = None
    rules = None

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('DBWriter', '')
        logger.info('Initiating DB Writer for: {}'.format(self.ftype))

        self.chunks = sorted(chunks)
        self.cm = ChunkManager(self.chunks)

    @timeit
    def write_to_db(self):
        logger.info('Completed Logic Checks for: {}'.format(self.ftype))
        while 1:
            try:
                df = self.cm.get_next_chunk()

                try:
                    # Write all these changes atomically
                    with transaction.atomic():
                        self._write_chunk(df)
                except ParserError as err:
                    logger.error(err)

            except IOError:
                break


    @timeit
    def _write_chunk(self, df):

        records = []
        for _, record in enumerate(df.to_dict('records')):
            records.append(self._create_record(record))
        
        for record in records:
            record.save()
        
        #TODO: find a way to use bulk_create
        #self.app_model.objects.bulk_create(records)


    def _create_record(self, record):
        """
        Return boolean for whether record was created
        """
        
        # Remove non-field keys in record dictionary
        field_values = self._extract_fields(record)
        
        try:
            record_object = self.app_model(**field_values)
        except Exception as err:
            logger.error(str(field_values))
            raise Exception(err)

        return record_object


    def _extract_fields(self, record):
        """
        Convert a dictionary of record values into a dictionary of
        Django model field values.
        """
        
        field_values = copy.deepcopy(record)
        
        # Deal with foreign key components in the record
        field_values = self._resolve_related_records(field_values)
        
        return field_values


    def _resolve_related_records(self, record):
        """
        Write records in code tables and other foreign key relationships
        Returns the record dictionary with changes as required
        """
        
        if logger.isEnabledFor(logging.DEBUG):
            for key in sorted(record.keys()): logger.debug('IN REC: {}: {}'.format(key, record[key]))
            for key in sorted(self.rules.foreign_key_fields_to_add.keys()):
                logger.debug('NEEDED AS FK: {}: {}'.format(key, record[key]))
        
        for lookup in self.rules.vlookups:
            lookup_data = lookup.resolve(record)
            if lookup_data:
                record.update(lookup_data)
            else:
                if lookup.get_key() in record:
                    del record[lookup.get_key()]
        
        for fk_field, (fk_model, fk_arg, is_primary_key) in self.rules.foreign_key_fields_to_add.items():
            
            value = record[fk_field]
            
            if isinstance(value, str) and not value and is_primary_key:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'Ignoring empty string foreign key: {fk_field}')
                del record[fk_field]
                continue
    
            if value == INT_NAN and is_primary_key:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'Ignoring NAN field for: {fk_field}')
                del record[fk_field]
                continue
    
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Could CHANGE MODEL TO USE `models.AutoField()` but not tampering (yet)!')
    
            # Since some are lists we need to manage them differently
            if type(value) == list:
    
                for item in value:
                    kwargs = self._get_fk_kwargs(fk_model, item, fk_arg, is_primary_key)
                    self._get(fk_model, kwargs)
    
                # Don't set the FK field here as already set as: value
    
            else:
                kwargs = self._get_fk_kwargs(fk_model, value, fk_arg, is_primary_key)
                fk_obj = self._get(fk_model, kwargs)
    
                # Now work out whether to set the FK object as the value or to just keep
                # the simple field. Have to do this if using the secondary database for extra
                # fields
                if fk_field not in self.rules.extended_fields.keys():
                    record[fk_field] = fk_obj

        return record


    def _get_fk_kwargs(self, fk_model, value, fk_arg, is_primary_key):
        
        if is_primary_key:
            kwargs = {'pk': value}
        else:
            pk = fk_model.objects.count()
            kwargs = {'pk': pk, fk_arg: value}

        return kwargs


    def _get(self, db_model, kwargs):

        model_class = db_model.__name__
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Writing {} with args: {}'.format(model_class, kwargs))
        
        try:
            obj = db_model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            logger.error(f'{db_model} not found with query: {kwargs}')

        return obj


class SourceConfigurationDBWriter(_DBWriterBase):

    app_model = SourceConfiguration
    rules = SourceConfigurationParserRules()


class StationConfigurationDBWriter(_DBWriterBase):

    app_model = StationConfiguration
    rules = StationConfigurationParserRules()


    def _extract_fields(self, record):
        """
        For Station Configuration we need to separate out each record into:
            1. Records for real StationConfiguration table
            2. Records sent in order to batch-populate the Header/Obs tables

        Intercept in this method and:
            1. Write the standard content to the StationConfiguration table
            2. Generate a separate writer to write records in the Deliveries DB table

        :param record: dictionary of items to write to DB record.
        :return: Boolean to indicate is record was created
        """
        
        record_copy = copy.deepcopy(record)
        # Deal with foreign key components in the record
        record_copy = self._resolve_related_records(record_copy)
        
        # Now split out into two dicts and write accordingly
        field_values, deliveries_record = self._extract_station_config_and_deliveries_dicts(record_copy)
        
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Writing extra info to deliveries DB: {}'.format(str(deliveries_record)))
        StationConfigurationLookupFields.objects.get_or_create(**deliveries_record)
        
        return field_values


    def _extract_station_config_and_deliveries_dicts(self, record):
        """
        Takes in a record from the delivery data set and returns a tuple of two
        dictionaries: (<station_config_dict>, <deliveries_db_dict>)

        :param record: Station Configuration record [dictionary]
        :return: Tuple of (<station_config_dict>, <deliveries_db_dict>)
        """
        main_record = record.copy()
        deliveries_record = OD()
        keys = sorted(main_record.keys())

        in_both_records = self.rules.extended_fields_to_duplicate

        for key in keys:
            if key in self.rules.extended_fields.keys() or key in in_both_records:
                deliveries_record[key] = main_record[key]

                if key not in in_both_records:
                    del main_record[key]

        return main_record, deliveries_record


class StationConfigurationOptionalDBWriter(_DBWriterBase):

    app_model = StationConfigurationOptional
    rules = StationConfigurationOptionalParserRules()


class HeaderTableDBWriter(_DBWriterBase):

    app_model = HeaderTable
    rules = HeaderTableParserRules()


class ObservationsTableDBWriter(_DBWriterBase):

    app_model = ObservationsTable
    rules = ObservationsTableParserRules()
