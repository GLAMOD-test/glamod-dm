'''
Created on Feb 15, 2019

@author: William Tucker
'''

import logging
import copy

from pandas.core.frame import DataFrame

from glamod.parser.utils import is_null, to_dict_dropna, timeit


logger = logging.getLogger(__name__)


class RecordManager:
    """ Parses CDM records from chunked data-frame collections. """
    
    def __init__(self, app_model, rules):
        
        self._app_model = app_model
        self._rules = rules
    
    def create_records(self, record_data_frame):
        """ Resolves Django model objects from a data frame of records.
        
        :return: A generator of unsaved records.
        """
        
        records = to_dict_dropna(record_data_frame)
        for field_values in records:
            
            try:
                record_object = self._app_model(**field_values)
            except Exception as err:
                logger.error(str(field_values))
                raise Exception(err)
            
            yield record_object
    
    @timeit
    def resolve_data_frame(self, record_data_frame):
        """ Resolves the records in a data frame.
        
        :return: A DataFrame object containing resolved record data.
        """
        
        records = record_data_frame.to_dict('records')
        
        # Resolve each record in the list and build a new data frame from them
        for index, record in enumerate(records):
            records[index] = self._resolve_missing_values(record)
        resolved_records = DataFrame(records)
        
        return resolved_records
    
    def _resolve_missing_values(self, record_data):
        """ Creates a new record from a dictionary of potential field values.
        
        :param record_data: dictionary of model field names and values
        """
        
        # Remove non-field keys in record dictionary
        field_values = copy.deepcopy(record_data)
        field_values = self._resolve_related_records(field_values)
        
        # Separate and save extended fields if any are found.
        field_values, extended_field_values = \
            self._separate_extended_fields(field_values)
        if extended_field_values:
            self._save_extended_fields(extended_field_values)
        
        return field_values
    
    @timeit
    def _resolve_related_records(self, field_values):
        """ Resolves foreign-key relationships according to custom rules.
        
        :param field_values: dictionary of model field names and values
        :return: The record dictionary with changes as required
        """
        
        for lookup in self._rules.lookups:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Resolving: {lookup}")
            
            resolved_value, extra_values = lookup.resolve(
                field_values, partial=True)
            
            field_values[lookup.get_key()] = resolved_value
            if extra_values:
                field_values.update(extra_values)
        
        return field_values
    
    def _separate_extended_fields(self, field_values):
        """ Separate extended fields from fields that are needed for the model.
        
        :param field_values: dictionary of model field names and values
        :return: Tuple of main record fields and extended fields
        """
        
        original_keys = list(field_values.keys())
        extended_fields = self._rules.extended_fields.keys()
        fields_to_duplicate = self._rules.extended_fields_to_duplicate
        
        extended_field_values = {}
        for key in original_keys:
            
            if key in extended_fields or key in fields_to_duplicate:
                if not is_null(field_values[key]):
                    # Add the extended field value to the new record dictionary
                    extended_field_values[key] = field_values[key]
                
                # Only keep duplicated fields in both dictionaries
                if key not in fields_to_duplicate:
                    del field_values[key]
        
        return field_values, extended_field_values
    
    def _save_extended_fields(self, extended_field_values):
        """ Saves extended fields to the database for future look-up.
        
        :param extended_field_values: dictionary of field values to save
        :return: True if the values were successfully saved
        """
        
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'Saving extended fields: {extended_field_values}')
        _, created = self._rules.extended_field_model.objects.get_or_create(
            **extended_field_values)
        
        return created
