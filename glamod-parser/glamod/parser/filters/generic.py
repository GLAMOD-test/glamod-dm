'''
Created on Mar 4, 2019

@author: William Tucker
'''

from .decorators import row_filter


def match_filter(key, match_value):
    
    @row_filter(key)
    def generated_filter(value):
        return value == match_value
    
    return generated_filter
