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
    
    def __init__(self, table_constraints):
        
        self._table_constraints = table_constraints
    
    def parse_value(self, column_name, value):
        
        if value != None and not self.is_null(value):
            
            parsed_value = value
            
            try:
                column_type = self._table_constraints.get_column_type(column_name)
                if not isinstance(value, column_type):
                    
                    if self._table_constraints.is_list_type(column_name):
                        column_type = self._table_constraints.get_column_item_type(
                                column_name)
                        
                        values_list = self.cell_value_to_list(str(value))
                        parsed_value = [self.convert(value, column_type)
                                        for value in values_list]
                        
                    else:
                        parsed_value = self.convert(value, column_type)
                
            except (ValueError, decimal.InvalidOperation) as e:
                raise ParserException(f"Failed to parse value for column '{column_name}'"
                                      f", entry {self._current_row}") from e
            
            return parsed_value
    
    @staticmethod
    def is_null(value):
        
        return value == 'NULL' or value == ''
    
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
