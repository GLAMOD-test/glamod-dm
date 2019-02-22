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
                 extra_fields=None):
        
        super().__init__(key)
        self._model = model
        self._matching_field = matching_field
        self._query_map = self._generate_full_query_map(query_map)
        self._extra_fields = extra_fields
    
    def resolve(self, record):
        
        query = self._build_query(record)
        if not query:
            return None, None
        
        resolved_object = self._resolve_object(query)
        return resolved_object, self._get_extra_values(resolved_object)
    
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
    
    def _get_extra_values(self, resolved_object):
        
        extra_values = {}
        if self._extra_fields:
            for record_field, lookup_field in self._extra_fields.items():
                extra_value = getattr(resolved_object, lookup_field)
                if not is_null(extra_value):
                    if hasattr(extra_value, 'pk'):
                        extra_values[record_field] = extra_value.pk
                    else:
                        extra_values[record_field] = extra_value
        
        return extra_values
    
    def __str__(self):
        return f"Lookup for field: {self._key}"


class OneToManyLookup(ForeignKeyLookup):
    
    def resolve(self, record):
        
        lookup_values = record.get(self._key)
        if not lookup_values:
            return [], None
        
        resolved_objects = []
        for value in lookup_values:
            query = self._build_query({ self._key: value })
            resolved_object = self._resolve_object(query)
            
            resolved_objects.append(resolved_object)
        
        return resolved_objects, None


class LinkedLookup(Lookup):
    
    def __init__(self, lookup=None, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(lookup, Lookup):
            raise ValueError(
                f"Invalid lookup value, {lookup}. Must be a Lookup.")
        self._lookup = lookup
    
    def resolve(self, record):
        
        resolved_object, extra_values = super().resolve(record)
        linked_resolved_object, linked_extra_values = self._lookup.resolve(resolved_object)
        
        return None, None


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
