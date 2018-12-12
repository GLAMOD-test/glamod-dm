import os
from collections import OrderedDict as OD
from importlib import import_module

import stringcase

from .utils import log, timeit, map_file_type

from .structure_check import (SourceAndStationConfigStructureCheck,
    HeaderAndObservationsTablesStructureCheck)
from .logic_check import (SourceConfigurationLogicCheck,
    StationConfigurationLogicCheck, HeaderTableLogicCheck,
    ObservationsTableLogicCheck)


class _DeliveryProcessorBase(object):

    CHECKS = OD()
    FILE_TYPES = []

    def __init__(self, location):
        self.location = location
        self.data_files = {}
        self.chunk_dict = {}

        self.file_types = self.CHECKS.keys()

        for ftype in self.FILE_TYPES:
            self.data_files[ftype] = []
            self.chunk_dict[ftype] = []

    def run(self):
        self._run_structure_checks()
        self._run_content_checks()
        self._run_logic_checks()
        self._write_to_db()

    @timeit
    def _run_structure_checks(self):
        for structure_check in self.STRUCTURE_CHECKS:

            s_check = structure_check(self.location)
            s_check.run()

            self._store_file_paths(s_check.get_files())

    @timeit
    def _run_content_checks(self):

        for ftype in self.FILE_TYPES:
            log('INFO', f'Content checks for files of type: {ftype}')

            for fpath in self.data_files[ftype]:

                content_check = self._get_content_check(fpath)
                content_check.run()

                chunks = content_check.chunks
                self.chunk_dict[ftype].extend(chunks)

    @timeit
    def _run_logic_checks(self):

        for ftype in self.FILE_TYPES:
            log('INFO', f'Logic checks for files of type: {ftype}')

            chunks = self.chunk_dict[ftype]
            logic_check_class = self._get_logic_check(chunks[0])

            logic_checker = logic_check_class(chunks)
            logic_checker.run()

    @timeit
    def _write_to_db(self):
        raise NotImplementedError

    def _store_file_paths(self, fpaths):
        for fpath in fpaths:

            ftype = self._get_key(fpath)
            self.data_files[ftype].append(fpath)

    def _get_key(self, path_or_cls):
        if type(path_or_cls) != str:
            path_or_cls = path_or_cls.__name__

        return map_file_type(path_or_cls)

    def _get_check_by_path(self, fpath, check_type, mod_name=None):
        class_name = map_file_type(fpath) + check_type

        if not mod_name:
            mod_name = stringcase.snakecase(check_type)

        mod = import_module('.' + mod_name, package='glamod.parser')
        return getattr(mod, class_name)

    def _get_content_check(self, fpath):
        return self._get_check_by_path(fpath, 'ContentCheck')(fpath)

    def _get_logic_check(self, chunk_path):
        return self._get_check_by_path(chunk_path, 'LogicCheck')

    def _get_db_writer(self, chunk_path):
        return self._get_check_by_path(chunk_path, 'DBWriter', mod_name='db_writer')



class SourceAndStationConfigProcessor(_DeliveryProcessorBase):

    FILE_TYPES = ['SourceConfiguration', 'StationConfiguration']
    STRUCTURE_CHECKS = [SourceAndStationConfigStructureCheck]
    LOGIC_CHECKS = [SourceConfigurationLogicCheck, StationConfigurationLogicCheck]

    @timeit
    def _write_to_db(self):

        for ftype in self.FILE_TYPES:
            log('INFO', f'Writing data to DB for files of type: {ftype}')

            chunks = self.chunk_dict[ftype]
            db_writer_class = self._get_db_writer(chunks[0])

            db_writer = db_writer_class(chunks)
            db_writer.write_to_db()



class HeaderAndObsTableProcessor(_DeliveryProcessorBase):

    FILE_TYPES = ['HeaderTable', 'ObservationsTable']
    STRUCTURE_CHECKS = [HeaderAndObservationsTablesStructureCheck]
    LOGIC_CHECKS = [HeaderTableLogicCheck, ObservationsTableLogicCheck]

    def _run_content_checks(self):
        super(HeaderAndObsTableProcessor, self)._run_content_checks()

    @timeit
    def _write_to_db(self):
        log('INFO', 'Loading data for Header Table files.')
        log('INFO', 'Loading data for Observation Table files.')
        
        for ftype in self.FILE_TYPES:
            log('INFO', f'Writing data to DB for files of type: {ftype}')

            chunks = self.chunk_dict[ftype]
            db_writer_class = self._get_db_writer(chunks[0])

            db_writer = db_writer_class(chunks)
            db_writer.write_to_db()
