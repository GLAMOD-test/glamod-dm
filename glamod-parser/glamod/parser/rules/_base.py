import logging

from glamod.parser.settings import INT_NAN
from collections import OrderedDict as OD
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class Lookup(object):
    
    def __init__(self, key, model, extra_fields=None):
        
        self._key = key
        self._model = model
        self._extra_fields = extra_fields
    
    @staticmethod
    def _is_null(value):
        
        if value is None: return True
        if value == INT_NAN: return True
        if isinstance(value, str) and not value: return True
        
        return False
    
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
                if not self._is_null(extra_value):
                    resolved[record_field] = extra_value
        
        return resolved
    
    def _resolve_object(self, query):
        
        try:
            return self._model.objects.get(**query)
        except ObjectDoesNotExist as e:
            logger.error((
                f"Referenced {self._model} object not found for field"
                f" '{self._key}'. The query was: {query}"
            ))
            raise e


class ForeignKeyLookup(Lookup):
    
    def __init__(self, key, model, lookup_key, extra_fields=None):
        
        super().__init__(key, model, extra_fields=extra_fields)
        self._lookup_key = lookup_key
    
    def _build_query(self, record):
        
        if self._key in record:
            lookup_value = record[self._key]
            if not self._is_null(lookup_value):
                return { self._lookup_key: lookup_value }


class OneToManyLookup(ForeignKeyLookup):
    
    def resolve(self, record):
        
        lookup_values = record.get(self._key)
        if not lookup_values:
            return []
        
        resolved_objects = []
        for value in lookup_values:
            query = { self._lookup_key: value }
            resolved_object = self._resolve_object(query)
            resolved_objects.append(getattr(resolved_object, self._lookup_key))
        
        return { self._key: resolved_objects }


class LinkedLookup(Lookup):
    
    def __init__(self, key, model, query_map, extra_fields=None):
        
        super().__init__(key, model, extra_fields=extra_fields)
        self._query_map = query_map
    
    def _build_query(self, record):
        
        linked_object = record[self._key]
        
        query = {}
        for linked_key, record_key in self._query_map.items():
            query[linked_key] = getattr(linked_object, record_key)
        
        return query
    
    def resolve(self, record):
        
        resolved = super().resolve(record)
        del resolved[self._key]
        
        return resolved


class _ParserRulesBase(object):

    _REQUIRED_PROPS = ('fields', 'index_field', 'code_table_fields')
    _EMPTY_PROPS_IF_NOT_THERE = ('extended_fields',
                                 'extended_fields_to_duplicate',
                                 'foreign_key_fields_to_add',
                                 'vlookup_fields')

    vlookups = []

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

        self.foreign_key_fields_to_add = self.code_table_fields

        assert(sorted(self.code_table_fields.keys()) == \
                      sorted(self.foreign_key_fields_to_add.keys()))


    def _set_expected_fields(self):
        self.expected_fields = deepcopy(self.fields)
        self.expected_fields.update(self.extended_fields)