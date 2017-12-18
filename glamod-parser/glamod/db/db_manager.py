'''
Created on Nov 28, 2017

@author: William Tucker
'''

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


maker = sessionmaker()

def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower() + "_ref"
    return name


class DBManager(object):
    
    def __init__(self, connection_string, schema):
        
        self._schema = schema
        
        self._engine = create_engine(connection_string)
        self._Base = automap_base()
        self._Base.prepare(self._engine, reflect=True, schema=schema,
                          name_for_scalar_relationship=name_for_scalar_relationship)
        
        maker.configure(bind=self._engine)
    
    def __enter__(self):
        
        self._session = maker()
        
        return self
    
    def __exit__(self, *args):
        
        self._session.close()
    
    def get_table(self, table_name):
        
        return self._Base.metadata.tables.get('.'.join([self._schema, table_name]))
    
    def get_model_class(self, class_name):
        
        return getattr(self._Base.classes, class_name)
    
    def merge(self, model_instance):
        
        self._session.merge(model_instance)
    
    def commit(self):
        
        self._session.commit()
