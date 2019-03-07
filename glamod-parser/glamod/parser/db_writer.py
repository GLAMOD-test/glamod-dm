import logging

from django.db import transaction
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

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
    
    def write_to_db(self, chunks, bulk=False):
        
        for chunk in chunks:
            try:
                # Write all these changes atomically
                with transaction.atomic():
                    self._write_chunk(chunk, bulk=bulk)
            except ParserError as err:
                logger.error(err)

    @timeit
    def _write_chunk(self, chunk, bulk=False):
        
        if bulk:
            try:
                chunk.to_sql(
                    self._table_name,
                    self._engine,
                    schema=self._schema,
                    if_exists='append',
                    chunksize=DB_CHUNK_SIZE,
                    index=False
                )
            except IntegrityError as e:
                logger.error((f'Failed to write chunk: '
                    f'{e.orig.diag.message_primary} '
                    f'({e.orig.diag.message_detail})'))
            
        else:
            for i in range(len(chunk)):
                try:
                    row = chunk.iloc[i:i+1]
                    row.to_sql(
                        self._table_name,
                        self._engine,
                        schema=self._schema,
                        if_exists='append',
                        index=False
                    )
                except IntegrityError as e:
                    logger.error((f'{e.orig.diag.message_primary} '
                        f'({e.orig.diag.message_detail})'))
