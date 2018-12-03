"""
test_complex_types.py
=====================

Tests for sub-classes of `complex_types._ComplexType`.

"""

import pytest

from glamod.parser.complex_types import *



def test_ReportIdType_success():
    values = ('0-20000-0-03979-1-2011-01-01T00:00',
              '0-20000-0-03979-1-2011-01-01',
              '0-20000-0-03979-1-2011-01')

    for value in values:
        # If no exception then it works
        x = ReportIdType(value)
        assert(x.value == value)


def test_ReportIdType_fail():
    err_msg_tmpl = 'Value provided "{}" does not match required pattern: "{}"'

    values = ('sdfdsfsdfdsfsdffs', '0-20000-0-03979-1-2011-0X')

    for value in values:
        with pytest.raises(ValueError) as exc_info:
            ReportIdType(value)
            assert(exc_info == err_msg_tmpl.format(value, ReportIdType._REGEX))

