from collections import OrderedDict as OD
from copy import deepcopy


class _ParserRulesBase(object):

    _REQUIRED_PROPS = ('fields', 'index_field', 'code_table_fields')
    _EMPTY_PROPS_IF_NOT_THERE = ('extended_fields',
                                 'extended_fields_to_duplicate',
                                 'foreign_key_fields_to_add',
                                 'vlookup_fields')

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