import os
import logging
import stringcase

from importlib import import_module
from cdmapp.models import SourceConfiguration, StationConfiguration, \
    StationConfigurationOptional, HeaderTable, ObservationsTable

from .settings import CHUNK_CACHE_DIR, CHUNK_CACHE_DIR_DEPTH
from .chunk_manager import ChunkManager
from .record_manager import RecordManager
from .utils import get_path_sub_dirs, timeit
from .db_writer import DBWriter
from .rules import (SourceConfigurationParserRules,
     StationConfigurationParserRules, StationConfigurationOptionalParserRules,
     HeaderTableParserRules, ObservationsTableParserRules)


logger = logging.getLogger(__name__)

class _DeliveryProcessorBase:
    
    _schema = 'cdm_v1'
    
    def __init__(self, location):
        
        self.location = location
        self.model_name = self._app_model.__name__
        
        data_dirs = get_path_sub_dirs(location, depth=CHUNK_CACHE_DIR_DEPTH)
        pickle_directory = os.path.join(CHUNK_CACHE_DIR, data_dirs)
        
        structure_check_class = self._get_check_by_name('StructureCheck')
        self._structure_check = structure_check_class(location)
        
        self._content_check_class = self._get_check_by_name('ContentCheck')
        self._logic_check_class = self._get_check_by_name('LogicCheck')
        
        self._chunk_manager = ChunkManager(pickle_directory)
        
        rules = self._rules_class()
        self._record_manager = RecordManager(self._app_model, rules)
        self._db_writer = DBWriter(
            self._record_manager, self._table_name, self._schema)

    def run(self):
        self._run_structure_checks()
        self._run_content_checks()
        self._run_logic_checks()

    @timeit
    def _run_structure_checks(self):
        
        logger.info(f'Structure checks for files of type: {self.model_name}')
        self._structure_check.run()
        self._data_files = self._structure_check.get_files()

    @timeit
    def _run_content_checks(self):

        logger.info(f'Content checks for files of type: {self.model_name}')
        for file_path in self._data_files:
            content_check = self._content_check_class(
                file_path, self._chunk_manager, self._record_manager)
            content_check.run()

    @timeit
    def _run_logic_checks(self):
        
        logger.info(f'Logic checks for files of type: {self.model_name}')
        logic_check = self._logic_check_class(self._chunk_manager)
        logic_check.run()

    @timeit
    def write_to_db(self, bulk):
        
        logger.info(f'Writing data to DB for files of type: {self.model_name}')
        chunks = self._chunk_manager.read_cached_chunks()
        self._db_writer.write_to_db(chunks, bulk=bulk)

    def _get_check_by_name(self, check_name):
        class_name = self.model_name + check_name
        
        module_name = stringcase.snakecase(check_name)
        module = import_module('.' + module_name, package='glamod.parser')
        
        return getattr(module, class_name)


class HeaderTableProcessor(_DeliveryProcessorBase):
    _app_model = HeaderTable
    _table_name = 'header_table'
    _rules_class = HeaderTableParserRules


class ObservationsTableProcessor(_DeliveryProcessorBase):
    _app_model = ObservationsTable
    _table_name = 'observations_table'
    _rules_class = ObservationsTableParserRules


class SourceConfigurationProcessor(_DeliveryProcessorBase):
    _app_model = SourceConfiguration
    _table_name = 'source_configuration'
    _rules_class = SourceConfigurationParserRules


class StationConfigurationProcessor(_DeliveryProcessorBase):
    _app_model = StationConfiguration
    _table_name = 'station_configuration'
    _rules_class = StationConfigurationParserRules


class StationConfigurationOptionalProcessor(_DeliveryProcessorBase):
    _app_model = StationConfigurationOptional
    _table_name = 'station_configuration_optional'
    _rules_class = StationConfigurationOptionalParserRules
