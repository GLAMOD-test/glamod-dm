"""
complex_types.py
================

Holds base class `_ComplexType` and a set of sub-classes that allow
complex validation when a data type is created from a value.

"""

import re


__all__ = ['LatitudeType', 'LongitudeType']


class _ComplexType(object):

    def __call__(self, value):
        "Call the instance, so it works like a function. Returns valid value."
        self._validate(value)
        if not hasattr(self, 'value'):
            raise Exception('ComplexType sub-class "{}" does not set ".value" properly.'
                            .format(self.__class__.__name__))

        return self.value

    def _validate(self, value):
        raise NotImplementedError

    def __str__(self):
        return str(self.value)



class _ComplexRegexType(_ComplexType):

    _REGEX = '.*'
    _ERR_TMPL = 'Value provided "{}" does not match required pattern: "{}"'

    def _validate(self, value):
        self._validate_by_regex(value)

    def _validate_by_regex(self, value):
        if re.match(self._REGEX, value):
            self.value = value
        else:
            raise ValueError(self._ERR_TMPL.format(value, self._REGEX))


class ReportIdType(_ComplexRegexType):

    _REGEX = '^\d-\d{5}-\d-[0-9a-zA-Z]{5}-\d-\d{4}-\d{2}(-\d{2}|-\d{2}T\d{2}:\d{2})?$'
    # E.g. 0-20000-0-03979-1-2011-01-01T00:00


class _ComplexRangeType(_ComplexType):

    _RANGE = (0, 1)
    _INCLUSIVE = True
    _ERR_TMPL = 'Value provided ({}) is out of range: ({} to {})'

    def _validate(self, value):
        self._validate_by_range(value)

    def _validate_by_range(self, value):
        self.value = float(value)
        low, high = self._RANGE

        if self._INCLUSIVE:
            if not (low <= self.value <= high):
                raise ValueError(self._ERR_TMPL.format(self.value, low, high))

        else:
            if not (low < self.value < high):
                raise ValueError(self._ERR_TMPL.format(self.value, low, high))



class LatitudeType(_ComplexRangeType):

    _RANGE = (-90, 90)
    _INCLUSIVE = True


class LongitudeType(_ComplexRangeType):

    _RANGE = (-180, 180)
    _INCLUSIVE = True