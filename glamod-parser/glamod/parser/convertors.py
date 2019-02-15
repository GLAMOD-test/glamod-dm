
from dateutil.parser import parse as timestamp
from functools import wraps

from glamod.parser.complex_types import *
from glamod.parser.settings import INT_NAN


__all__ = ['str_strip', 'int_or_empty', 'float_or_empty', 'timestamp_or_empty',
           'list_of_ints', 'list_of_strs']


def prestrip(func):
    @wraps(func)
    def _wrapped_strip(*args, **kwargs):
        args = tuple([args[0].strip()] + list(args[1:]))
        return func(*args, **kwargs)

    return _wrapped_strip


@prestrip
def str_strip(value):
    return str(value)


def _x_or_empty(value, conv_func, default=INT_NAN):
    if value == '':
        return default

    return conv_func(value)


def int_or_empty(value):
    return _x_or_empty(value, int)
    

def float_or_empty(value):
    return _x_or_empty(value, float)


def timestamp_or_empty(value):
    return _x_or_empty(value, timestamp, default=None)


def _as_list(value):
    value = value.strip('{} ')
    return [_ for _ in value.split(',') if _ != '']


@prestrip
def list_of_ints(value):
    return [int(_) for _ in _as_list(value)]


def list_of_strs(value):
    return [str(_) for _ in _as_list(value)]



# Add all complex type convertors as one_liners
latitude = LatitudeType()
longitude = LongitudeType()