'''
Created on Nov 28, 2017

@author: William Tucker
'''

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower() + "_ref"
    return name


class DBManager(object):
    
    def __init__(self, connection_string, schema):
        self.schema = schema
        
        self._engine = create_engine(connection_string)
        self._Base = automap_base()
        self._Base.prepare(self._engine, reflect=True, schema=schema,
                          name_for_scalar_relationship=name_for_scalar_relationship)
    
    def start_session(self):
        
        self._session = Session(self._engine)
    
    def close_session(self):
        
        self._session.close()
    
    def get_table(self, table_name):
        
        return self._Base.metadata.tables.get('.'.join([self.schema, table_name]))
    
    def get_model_class(self, class_name):
        
        return getattr(self._Base.classes, class_name)
    
    def add(self, model_instance):
        
        self._session.add(model_instance)
        self._session.commit()
