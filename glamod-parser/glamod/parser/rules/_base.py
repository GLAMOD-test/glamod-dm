import logging

from glamod.parser.utils import is_null
from collections import OrderedDict as OD
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class Lookup:
    
    def __init__(self, key):
        
        self._key = key
    
    def get_key(self):
        
        return self._key
    
    def resolve(self, record):
        
        raise NotImplementedError()


class ForeignKeyLookup(Lookup):
    
    def __init__(self, key, model, matching_field, query_map=None,
                 extra_fields=None, default=None):
        
        super().__init__(key)
        self._model = model
        self._matching_field = matching_field
        self._query_map = self._generate_full_query_map(query_map)
        self._extra_fields = extra_fields
        self._default = default
    
    def resolve(self, record, partial=False):
        
        value = self._default
        
        query = self._build_query(record)
        if not query:
            return value, None
        
        resolved_object = self._resolve_object(query)
        if resolved_object:
            if partial:
                value = resolved_object.pk
            else:
                value = resolved_object
        extra_values = self._get_extra_values(resolved_object, partial=partial)
        
        return value, extra_values
    
    def _build_query(self, record):
        
        query = {}
        for key, matching_field in self._query_map.items():
            
            if isinstance(record, dict):
                lookup_value = record.get(key)
            else:
                lookup_value = getattr(record, key)
            
            if is_null(lookup_value):
                if key == self._key:
                    # Return nothing if the primary lookup value is missing
                    return None
            else:
                query[matching_field] = lookup_value
        
        if query:
            return query
    
    def _generate_full_query_map(self, partial_query_map):
        
        query_map = {}
        if self._matching_field:
            query_map[self._key] = self._matching_field
        
        if partial_query_map:
            query_map.update(partial_query_map)
        
        return query_map
    
    def _resolve_object(self, query):
        
        try:
            return self._model.objects.get(**query)
        except ObjectDoesNotExist as e:
            logger.error((
                f"Referenced {self._model} object not found for field"
                f" '{self._key}'. The query was: {query}"
            ))
            raise e
    
    def _get_extra_values(self, resolved_object, partial=False):
        
        values = {}
        if self._extra_fields:
            for record_field, lookup_field in self._extra_fields.items():
                value = getattr(resolved_object, lookup_field)
                
                if partial and hasattr(value, 'pk'):
                    values[record_field] = value.pk
                elif not is_null(value):
                    values[record_field] = value
        
        return values
    
    def __str__(self):
        return f"Lookup for field: {self._key}"


class OneToManyLookup(ForeignKeyLookup):
    
    def resolve(self, record, partial=False):
        
        lookup_values = record.get(self._key)
        if not lookup_values:
            return [], None
        
        resolved_values = []
        for value in lookup_values:
            query = self._build_query({ self._key: value })
            resolved_object = self._resolve_object(query)
            if resolved_object:
                if partial:
                    value = resolved_object.pk
                else:
                    value = resolved_object
            
            resolved_values.append(value)
        
        return resolved_values, None


class _ParserRulesBase(object):

    _REQUIRED_PROPS = ('fields', 'index_field', 'lookups')
    _EMPTY_PROPS_IF_NOT_THERE = ('extended_fields',
                                 'extended_fields_to_duplicate')

    lookups = []

    def __init__(self):
        self._validate()

        self._set_expected_fields()

    def _validate(self):
        "Validate contents."
        for prop in self._EMPTY_PROPS_IF_NOT_THERE:
            if not hasattr(self, prop):
                setattr(self, prop, OD())

        for prop in self._REQUIRED_PROPS:
            if not hasattr(self, prop):
                raise Exception('Parser: {} is missing property: {}'.format(
                    self.__class__.__name__, prop))

        if not hasattr(self, 'extended_fields'):
            self.extended_fields = OD()


    def _set_expected_fields(self):
        self.expected_fields = deepcopy(self.fields)
        self.expected_fields.update(self.extended_fields)
