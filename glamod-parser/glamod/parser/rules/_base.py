import logging

from glamod.parser.utils import is_null
from collections import OrderedDict as OD
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class Lookup(object):
    
    def __init__(self, key, model, matching_field, query_map=None,
                 extra_fields=None, resolve_basic=False):
        
        self._key = key
        self._model = model
        self._matching_field = matching_field
        self._query_map = self._generate_full_query_map(query_map)
        self._extra_fields = extra_fields
        self._resolve_basic = resolve_basic
    
    def get_key(self):
        
        return self._key
    
    def resolve(self, record):
        
        query = self._build_query(record)
        if not query:
            return None
        
        resolved_object = self._resolve_object(query)
        
        resolved = {}
        resolved[self._key] = resolved_object
        
        if self._extra_fields:
            for record_field, lookup_field in self._extra_fields.items():
                extra_value = getattr(resolved_object, lookup_field)
                if not is_null(extra_value):
                    resolved[record_field] = extra_value
        
        return resolved
    
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
    
    def __str__(self):
        return f"Lookup for field: {self._key}"


class ForeignKeyLookup(Lookup):
    pass


class OneToManyLookup(ForeignKeyLookup):
    
    def resolve(self, record):
        
        lookup_values = record.get(self._key)
        if not lookup_values:
            return []
        
        resolved_objects = []
        for value in lookup_values:
            query = self._build_query({ self._key: value })
            resolved_object = self._resolve_object(query)
            
            if self._resolve_basic:
                resolved_objects.append(value)
            else:
                resolved_objects.append(resolved_object)
        
        return { self._key: resolved_objects }


class LinkedLookup(Lookup):
    
    def __init__(self, linked_through, lookup):
        
        if not isinstance(lookup, Lookup):
            raise ValueError("Invalid linked_through value. Must be a Lookup.")
        
        self._linked_through = linked_through
        self._lookup = lookup
    
    def resolve(self, record):
        
        linked_record = record.get(self._linked_through)
        if not linked_record:
            raise ValueError(f"Record is missing key: {self._linked_through}")
        
        resolved = self._lookup.resolve(linked_record)
        del resolved[self._lookup.get_key()]
        
        return resolved


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
