"""
test_utils.py
=====================

Tests for functions in `utils.py`.

"""

import pytest

from glamod.parser.utils import *
from glamod.parser.content_check import *


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
 

