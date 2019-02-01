
import os
import re
import logging


from .utils import count_lines, report_errors
from .exceptions import ParserError
from .settings import REGEX_SAFE


logger = logging.getLogger(__name__)


class _StructureCheck(object):

    _EXPECTED_DIRS = []
    _EXPECTED_FILES = []
    

    def __init__(self, top_dir):
        self.top_dir = top_dir
        self._contents = os.listdir(self.top_dir)
 
        # The self._files property will be populated during the checks
        self._files = []


    def run(self):        
        self._validate()


    def _validate(self):
        # Run all the checks
        self._validate_sub_dirs()
        self._validate_file_existence()

        # Run specific extras
        self._specific_checks()

    
    def get_files(self):
        return self._files


    def _specific_checks(self):
        "To be over-ridden in sub-classes."
        raise NotImplementedError()


    def _validate_sub_dirs(self):
        errs = []

        for dr in self._EXPECTED_DIRS:
            if dr not in self._contents:
                errs.append('Required directory "{}" not found in delivery'.format(dr))

        extras = set(self._EXPECTED_DIRS).symmetric_difference(set(self._contents))

        if extras:
            logger.warn('Unexpected directories found: {}'.format(str(extras)))

        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating directory: {}:'
                              '{}'.format(self.top_dir, err_string))
          
        logger.info('Checked: directory structure.')


    def _validate_file_existence(self):

        errs = []
        found_files = []

        for dr in self._EXPECTED_DIRS:
            for fname in os.listdir(dr):
                found_files.append(os.path.join(dr, fname))

        for exp in self._EXPECTED_FILES: 
            found = False
            for found in found_files:
                if re.match(exp, os.path.basename(found)):
                    self._files.append(found)
                    found = True
            if not found:
                errs.append('[ERROR] File with pattern "{}" not found'.format(exp))
 
        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating files: {}:'
                              '{}'.format(self.top_dir, err_string))

        logger.info('Checked file structure (not content yet).')


class SourceAndStationConfigStructureCheck(_StructureCheck):

    _EXPECTED_DIRS = [
        'source_configuration',
        'station_configuration',
    ]
    _EXPECTED_FILES = [
        'source_configuration_({}+)\.psv'.format(REGEX_SAFE),
        'station_configuration_({}+)\.psv'.format(REGEX_SAFE),
    ]


    def _specific_checks(self):
        pass


class HeaderAndObservationsTablesStructureCheck(_StructureCheck):

    _EXPECTED_DIRS = [
        'header_table',
        'observations_table',
    ]
    _EXPECTED_FILES = [
        'header_table_.*\.psv',
        'observations_table_.*\.psv',
    ]


    def _specific_checks(self):
        self._validate_file_lengths()


    def _validate_file_lengths(self):
        'Check that all header and observation tables have equal number of records.'

        errs = []
        found_files = self._files[2:]

        while found_files:
            _f1, _f2 = found_files[:2]
            found_files = found_files[2:]

            if count_lines(_f1) != count_lines(_f2):
                errs.append('[ERROR] Line counts must be the same for:\n\t{}'
                            '\n\t and: {}'.format(_f1, _f2))

        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating files: {}:'
                              '{}'.format(self.top_dir, err_string))

        logger.info('Checked file structure (not content yet).')
