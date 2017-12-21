'''
Created on Dec 13, 2017

@author: William Tucker
'''

import re
import decimal

from dateutil.parser import parse as dateutil_parse
from datetime import datetime

from glamod.parser.exceptions import ParserException


class FileParser(object):
    
    DEFAULT_NULL_VALUE = 'NULL'
    
    def __init__(self, table_constraints, null_values=None, use_default_null=True):
        
        self._table_constraints = table_constraints
        
        self._null_values = []
        if use_default_null:
            self._null_values.append(self.DEFAULT_NULL_VALUE)
        
        if null_values and len(null_values) > 0:
            self._null_values += null_values
    
    def parse_value(self, column_name, value):
        
        parsed_value = None
        if value != None and not value in self._null_values:
            try:
                column_type = self._table_constraints.get_column_type(column_name)
                if isinstance(value, column_type):
                    parsed_value = value
                    
                elif value:
                    if self._table_constraints.is_list_type(column_name):
                        column_type = self._table_constraints.get_column_item_type(
                                column_name)
                        
                        values_list = self.cell_value_to_list(str(value))
                        parsed_value = [self.convert(value, column_type)
                                        for value in values_list]
                    else:
                        parsed_value = self.convert(value, column_type)
                
            except (ValueError, decimal.InvalidOperation) as e:
                raise ParserException(f"Failed to parse value '{value}' to {column_type} "
                                      f"for column '{column_name}'") from e
        
        return parsed_value
    
    @staticmethod
    def convert(value, data_type):
        
        if data_type == datetime:
            return FileParser.parse_datetime(value)
        else:
            return data_type(value)
    
    @staticmethod
    def cell_value_to_list(value, delimiter=','):
        
        expression = re.compile('^{(.*)}$')
        match = expression.match(value)
        
        if match:
            if match.group(1):
                return match.group(1).split(delimiter)
            else:
                return []
        else:
            return [value]
    
    @staticmethod
    def parse_datetime(value):
        
        try:
            return datetime(value)
            
        except TypeError:
            
            if (isinstance(value, int)):
                return datetime(value, 1, 1)
            else:
                try:
                    return dateutil_parse(value)
                except TypeError:
                    raise(ValueError(f"Invalid datetime format: {value}"))
