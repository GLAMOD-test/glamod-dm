
import os
import re


from glamod.parser.utils import count_lines, report_errors
from glamod.parser.exceptions import ParserError
from glamod.parser.settings import REGEX_SAFE


class _StructureCheck(object):

    _EXPECTED_FILES = []
    

    def __init__(self, top_dir):
        self.top_dir = top_dir
        self._contents = os.listdir(self.top_dir)
 
        # The self._files property will be populated during the checks
        self._files = []
        
        self._validate()


    def _validate(self):
        # Run all the checks
        self._validate_sub_dirs()
        self._validate_file_existence()

        # Run specific extras
        self._specific_checks()


    def _specific_checks(self):
        "To be over-ridden in sub-classes."
        raise NotImplementedError()


    def _validate_sub_dirs(self):
        expected_dirs = set([os.path.dirname(path) for path in self._EXPECTED_FILES])
        errs = []

        for dr in expected_dirs:
            if dr not in self._contents:
                errs.append('Required directory "{}" not found in delivery'.format(dr))

        extras = set(expected_dirs).symmetric_difference(set(self._contents))

        if extras:
            errs.append('Unexpected directories found: {}'.format(str(extras)))

        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating directory: {}:'
                              '{}'.format(self.top_dir, err_string))
          
        print('[INFO] Checked: directory structure.')


    def _validate_file_existence(self):

        errs = []
        found_files = []

        for root, subdirs, files in os.walk(self.top_dir):
            for fname in files:
                found_files.append(os.path.join(root, fname))

        for exp in self._EXPECTED_FILES: 
            for found in found_files:
                if re.match(exp, found.replace(self.top_dir + '/', '')):
                    self._files.append(found)
                    break
            else:
                errs.append('[ERROR] File with pattern "{}" not found'.format(exp))
 
        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating files: {}:'
                              '{}'.format(self.top_dir, err_string))

        print('[INFO] Checked file structure (not content yet).')


class SourceAndStationConfigStructureCheck(_StructureCheck):

    _EXPECTED_FILES = [
        'source_configuration/source_configuration_({}+)\.psv'.format(REGEX_SAFE),
        'station_configuration/station_configuration_({}+)\.psv'.format(REGEX_SAFE) ]

    def _specific_checks(self):
        pass


class CompleteStructureCheck(_StructureCheck):

    _EXPECTED_FILES = [
        'source_configuration/source_configuration_({}+)\.psv'.format(REGEX_SAFE),
        'station_configuration/station_configuration_({}+)\.psv'.format(REGEX_SAFE),
        'header_table/header_table_.*\.psv', 
        'observations_table/observations_table_.*\.psv' ]


    def _specific_checks(self):
        pass #self._validate_file_lengths()


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

        print('[INFO] Checked file structure (not content yet).')

