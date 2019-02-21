import logging

from django.db import transaction

from .utils import timeit
from .exceptions import ParserError


logger = logging.getLogger(__name__)


class DBWriter(object):
    
    def __init__(self, record_manager):
        
        self._record_manager = record_manager
    
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
        
        for record in self._record_manager.create_records(chunk):
            record.save()
        
        #TODO: find a way to use bulk_create
        #self.app_model.objects.bulk_create(records)
