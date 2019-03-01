'''
Created on Feb 28, 2019

@author: William Tucker
'''

import pandas

from functools import wraps


def row_filter(*keys):
    
    def row_filter_decorator(func):
        
        @wraps(func)
        def wrapper(row, **kwargs):
            
            values = []
            for key in keys:
                
                value = row[key]
                if pandas.isnull(value):
                    return True
                values.append(value)
            
            return func(*values, **kwargs)
        
        return wrapper
    
    return row_filter_decorator


def match_filter(key, match_value):
    
    @row_filter(key)
    def generated_filter(value):
        return value == match_value
    
    return generated_filter

