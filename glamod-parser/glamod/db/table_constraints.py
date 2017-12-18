'''
Created on Nov 29, 2017

@author: William Tucker
'''

from sqlalchemy.types import ARRAY


class TableConstraints(object):
    
    def __init__(self, table):
        
        self.name = table.name
        
        self._column_types = {}
        for column in table.columns:
            self._column_types[column.name] = column.type
        
        self._table = table
    
    def is_column(self, column_name):
        
        return column_name in self._table.columns
    
    def is_primary_key(self, column_name):
        
        return self._table.columns[column_name].primary_key
    
    def is_list_type(self, column_name):
        
        column_type = self._column_types[column_name]
        return isinstance(column_type, ARRAY)
    
    def get_column_type(self, column_name):
        
        return self._column_types[column_name].python_type
    
    def get_column_item_type(self, column_name):
        
        return self._column_types[column_name].item_type.python_type
