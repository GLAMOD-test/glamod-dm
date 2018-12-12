import copy
from collections import OrderedDict as OD

from django.db import transaction


from glamod.parser.settings import *
from glamod.parser.utils import log, timeit
from glamod.parser.chunk_manager import ChunkManager

from glamod.parser.rules import (SourceConfigurationParserRules,
    StationConfigurationParserRules, HeaderTableParserRules,
    ObservationsTableParserRules)


class _DBWriterBase(object):

    app_model = None
    rules = None

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('DBWriter', '')
        log('INFO', 'Initiating DB Writer for: {}'.format(self.ftype))

        self.chunks = sorted(chunks)
        self.cm = ChunkManager(self.chunks)

    @timeit
    def write_to_db(self):
        log('INFO', 'Completed Logic Checks for: {}'.format(self.ftype))
        while 1:
            try:
                df = self.cm.get_next_chunk()

                try:
                    # Write all these changes atomically
                    with transaction.atomic():
                        self._write_chunk(df)
                except Exception as err:
                    raise Exception(err)

            except IOError:
                break


    def _write_chunk(self, df):

        for count, record in enumerate(df.to_dict('records')):
            print(f'Writing record: {count + 1:5d}')

            created = self._write_record(record)
            print('Was it created? {}'.format(str(created)))


    def _write_record(self, record):
        # Deal with foreign key components in the record first
        # Return boolean for whether record was created
        rec = self._resolve_related_records(record)

        try:
            _, created = self.app_model.objects.get_or_create(**rec)
        except Exception as err:
            print(str(rec))
            raise Exception(err)

        return created


    def _resolve_related_records(self, record):
        # Write records in code tables and other foreign key relationships
        # Returns the record dictionary with changes as required
        rec = copy.deepcopy(record)

        for key in sorted(record.keys()): print('IN REC: {}: {}'.format(key, record[key]))
        for key in sorted(self.rules.foreign_key_fields_to_add.keys()):
            print('NEEDED AS FK: {}: {}'.format(key, record[key]))

        for fk_field, (fk_model, fk_arg, is_primary_key) in self.rules.foreign_key_fields_to_add.items():

#            if fk_field == 'region':
#                import pdb; pdb.set_trace()

            value = rec[fk_field]

            if isinstance(value, str) and not value and is_primary_key:
                log('DEBUG', f'Ignoring empty string foreign key: {fk_field}')
                del rec[fk_field]
                continue

            if value == INT_NAN and is_primary_key:
                log('DEBUG', f'Ignoring NAN field for: {fk_field}')
                del rec[fk_field]
                continue

            log('WARN', 'Could CHANGE MODEL TO USE `models.AutoField()` but not tampering (yet)!')

            # Since some are lists we need to manage them differently
            if type(value) == list:

                for item in value:
                    kwargs = self._get_fk_kwargs(fk_model, item, fk_arg, is_primary_key)
                    self._get_or_create(fk_model, kwargs)

                # Don't set the FK field here as already set as: value

            else:
                kwargs = self._get_fk_kwargs(fk_model, value, fk_arg, is_primary_key)
                fk_obj = self._get_or_create(fk_model, kwargs)

                # Now work out whether to set the FK object as the value or to just keep
                # the simple field. Have to do this if using the secondary database for extra
                # fields
                if fk_field not in self.rules.extended_fields.keys():
                    rec[fk_field] = fk_obj

        return rec


    def _get_fk_kwargs(self, fk_model, value, fk_arg, is_primary_key):
        if is_primary_key:
            kwargs = {'pk': value}
        else:
            pk = fk_model.objects.count()
            kwargs = {'pk': pk, fk_arg: value}

        return kwargs


    def _get_or_create(self, db_model, kwargs):

        model_class = db_model.__name__
        log('DEBUG', 'Writing {} with args: {}'.format(model_class, kwargs))
        obj, created = db_model.objects.get_or_create(**kwargs)

        if created:
            log('INFO', 'Created record: {} (type: {})'.format(obj, model_class))

        return obj


class SourceConfigurationDBWriter(_DBWriterBase):

    app_model = SourceConfiguration
    rules = SourceConfigurationParserRules()

#    def write_to_db(self):
#        log('WARN', 'DISABLED FOR: {}!!!!!'.format(self.ftype))


class StationConfigurationDBWriter(_DBWriterBase):

    app_model = StationConfiguration
    rules = StationConfigurationParserRules()


    def _write_record(self, record):
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
        # Deal with foreign key components in the record first
        # Return boolean for whether record was created
        rec = self._resolve_related_records(record)

        # Now split out into two dicts and write accordingly
        main_record, deliveries_record = self._extract_station_config_and_deliveries_dicts(rec)

        log('INFO', 'Writing extra info to deliveries DB: {}'.format(str(deliveries_record)))
        StationConfigurationLookupFields.objects.using('deliveries_db').get_or_create(**deliveries_record)

        try:
            log('INFO', 'Writing main record: {}'.format(str(main_record)))
            _, created = self.app_model.objects.get_or_create(**main_record)
        except Exception as err:
            log('ERROR', 'MAIN RECORD FAILED TO WRITE: {}'.format(str(main_record)))
            raise Exception(main_record)

        return created


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



class HeaderTableDBWriter(_DBWriterBase):

    app_model = HeaderTable
    rules = HeaderTableParserRules()


class ObservationsTableDBWriter(_DBWriterBase):

    app_model = ObservationsTable
    rules = ObservationsTableParserRules()
