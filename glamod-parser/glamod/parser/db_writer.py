import logging

from django.db import transaction
from cdmapp.models import SourceConfiguration, StationConfiguration, \
    StationConfigurationOptional, HeaderTable, ObservationsTable

from glamod.parser.utils import timeit
from glamod.parser.chunk_manager import ChunkManager
from glamod.parser.record_manager import RecordManager
from glamod.parser.exceptions import ParserError
from glamod.parser.rules import (SourceConfigurationParserRules,
    StationConfigurationParserRules, StationConfigurationOptionalParserRules,
    HeaderTableParserRules, ObservationsTableParserRules)


logger = logging.getLogger(__name__)


class _DBWriterBase(object):

    app_model = None
    rules = None

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('DBWriter', '')
        logger.info('Initiating DB Writer for: {}'.format(self.ftype))

        self.chunks = sorted(chunks)
        self.cm = ChunkManager(self.chunks)

    @timeit
    def write_to_db(self):
        logger.info('Writing chunks for: {}'.format(self.ftype))
        
        for chunked_df in self.cm.read_chunks():
            try:
                # Write all these changes atomically
                with transaction.atomic():
                    self._write_chunk(chunked_df)
            except ParserError as err:
                logger.error(err)


    @timeit
    def _write_chunk(self, chunked_df):
        
        record_manager = RecordManager(chunked_df, self.app_model, self.rules)
        
        for record in record_manager.resolve_records():
            record.save()
        
        #TODO: find a way to use bulk_create
        #self.app_model.objects.bulk_create(records)


class SourceConfigurationDBWriter(_DBWriterBase):

    app_model = SourceConfiguration
    rules = SourceConfigurationParserRules()


class StationConfigurationDBWriter(_DBWriterBase):

    app_model = StationConfiguration
    rules = StationConfigurationParserRules()


class StationConfigurationOptionalDBWriter(_DBWriterBase):

    app_model = StationConfigurationOptional
    rules = StationConfigurationOptionalParserRules()


class HeaderTableDBWriter(_DBWriterBase):

    app_model = HeaderTable
    rules = HeaderTableParserRules()


class ObservationsTableDBWriter(_DBWriterBase):

    app_model = ObservationsTable
    rules = ObservationsTableParserRules()
