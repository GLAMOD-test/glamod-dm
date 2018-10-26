from collections import OrderedDict as OD
from copy import deepcopy


class _ParserRulesBase(object):

    _REQUIRED_PROPS = ('fields', 'index_field', 'code_table_fields')

    def __init__(self):
        self._validate()

        self._set_expected_fields()

    def _validate(self):
        "Validate contents."
        for prop in self._REQUIRED_PROPS:
            if not hasattr(self, prop):
                raise Exception('Parser: {} is missing property: {}'.format(
                    self.__class__.__name__, prop))

        if not hasattr(self, 'extended_fields'):
            self.extended_fields = OD()

    def _set_expected_fields(self):
        self.expected_fields = deepcopy(self.fields)
        self.expected_fields.update(self.extended_fields)