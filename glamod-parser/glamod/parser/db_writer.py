import logging

from django.db import transaction
from sqlalchemy import create_engine

from .utils import timeit
from .exceptions import ParserError
from .settings import DB_CHUNK_SIZE, DATABASE


DATABASE_CONNECTION_TEMPLATE = \
    'postgresql://{user}:{password}@{host}:{port}/{name}'

logger = logging.getLogger(__name__)


class DBWriter(object):
    
    def __init__(self, record_manager, table_name, schema=None):
        
        self._record_manager = record_manager
        self._table_name = table_name
        self._schema = schema
        
        database_connection = DATABASE_CONNECTION_TEMPLATE.format(**DATABASE)
        self._engine = create_engine(database_connection)
    
    def write_to_db(self, chunks):
        
        for chunk in chunks:
            try:
                # Write all these changes atomically
                with transaction.atomic():
                    self._write_chunk(chunk)
            except ParserError as err:
                logger.error(err)

    @timeit
    def _write_chunk(self, chunk):
        
        records = chunk.to_dict(orient='rows')
        
        chunk.to_sql(
            self._table_name,
            self._engine,
            schema=self._schema,
            if_exists='append',
            chunksize=DB_CHUNK_SIZE,
            index=False
        )
