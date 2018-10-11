
import numpy

from glamod.parser.settings import INT_NAN


def int_or_empty(value):
    if value == '':
        return INT_NAN
    else:
        return int(value)



