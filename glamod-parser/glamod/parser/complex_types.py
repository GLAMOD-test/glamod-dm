"""
complex_types.py
================

Holds base class `_ComplexType` and a set of sub-classes that allow
complex validation when a data type is created from a value.

"""

import re


class _ComplexType(object):

    def __init__(self, value):
        self._validate(value)

    def _validate(self, value):
        raise NotImplementedError

    def _validate_by_regex(self, value):
        if re.match(self._REGEX, value):
            self.value = value
        else:
            raise ValueError('Value provided "{}" does not match required pattern: "{}"'.format(
                            value, self._REGEX))

    def __str__(self):
        return str(self.value)


class ReportIdType(_ComplexType):

    _REGEX = '^\d-\d{5}-\d-[0-9a-zA-Z]{5}-\d-\d{4}-\d{2}(-\d{2}|-\d{2}T\d{2}:\d{2})?$'
# E.g. 0-20000-0-03979-1-2011-01-01T00:00

    def _validate(self, value):
        self._validate_by_regex(value) 


