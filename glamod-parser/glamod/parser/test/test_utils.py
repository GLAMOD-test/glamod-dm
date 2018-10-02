"""
test_utils.py
=====================

Tests for functions in `utils.py`.

"""

import pytest

from glamod.parser.utils import *
from glamod.parser.content_check import *
 

def test_get_content_check_success():
    args = [
        ('source_configuration_test001.psv', SourceConfigurationContentCheck),
        ('station_configuration/station_configuration_test001.psv', StationConfigurationContentCheck)
    ]

    for fpath, cls in args:
        resp = get_content_check(fpath) 
        assert(resp.__class__.__name__ == cls.__name__)


def test_field_to_db_model():
    args = [('source_format', 'SourceFormat')]
 
    for field, model_name in args:
        resp = field_to_db_model(field)
        assert(resp == model_name)


def test_db_model_to_field():
    args = [('StationConfigurationFields', 'station_configuration_fields')]

    for model_name, field in args:
        resp = db_model_to_field(model_name)
        assert(resp == field)
 

