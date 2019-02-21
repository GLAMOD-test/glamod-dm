"""
Plan for generic content check:

1. Check column names are correct
2. In rules, define an instance of FieldCheck
3. Parse each record and cycle through FieldCheck instances

"""

import os
import logging

from glamod.parser.file_parser import FileParser
from glamod.parser.rules import (
     SourceConfigurationParserRules, StationConfigurationParserRules,
     StationConfigurationOptionalParserRules,
     HeaderTableParserRules, ObservationsTableParserRules)


logger = logging.getLogger(__name__)


class _ContentCheck(object):

    _rules = None

    def __init__(self, file_path, chunk_manager, record_manager):
        self._file_path = file_path
        self._cls = self.__class__.__name__
        self._chunk_manager = chunk_manager
        self._record_manager = record_manager


    def run(self):
        logger.info('Starting {} on: {}'.format(self._cls, self._file_path))
        self._parser = FileParser(self._file_path)
        
        # Check column names are correct
        self._check_column_names()

        # Now cache chunks on the file system
        self._resolve_and_cache_chunks()
        
        logger.info('Completed {} on: {}'.format(self._cls, self._file_path))


    def get_chunks(self):
        return self._chunk_manager


    def _check_column_names(self):
        expected = [key for key in self._rules.expected_fields.keys()]
        actual = self._parser.get_column_names()

        if expected != actual:
            diff = list(set(expected).symmetric_difference(actual)) 
            raise Exception('Column names are incorrect in file: {}'
                            '\n\n\tShould be: {}\n\n\tThe DIFFERENCE was '
                            'identified as: {}'.format(
                            self._file_path, expected, diff))


    def _resolve_and_cache_chunks(self):
        
        # Read in and cache the data as pickled chunks
        _fields = self._rules.expected_fields
        chunks = self._parser.read_chunks(convertors=_fields)
        
        chunk_name = os.path.splitext(os.path.basename(self._file_path))[0]
        self._chunk_manager.pickle_chunks(
            chunks, chunk_name, self._record_manager)


class SourceConfigurationContentCheck(_ContentCheck):
    _rules = SourceConfigurationParserRules()


class StationConfigurationContentCheck(_ContentCheck):
    _rules = StationConfigurationParserRules()


class StationConfigurationOptionalContentCheck(_ContentCheck):
    _rules = StationConfigurationOptionalParserRules()


class HeaderTableContentCheck(_ContentCheck):
    _rules = HeaderTableParserRules()


class ObservationsTableContentCheck(_ContentCheck):
    _rules = ObservationsTableParserRules()
