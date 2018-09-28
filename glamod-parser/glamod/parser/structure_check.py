
import os


from glamod.parser.exceptions import ParserError
from glamod.parser.settings import REGEX_SAFE


class _StructureCheck(object):

    _EXPECTED_DIRS = []
    _EXPECTED_FILES = []
    
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self._contents = os.listdir(self.top_dir)
        
        self._validate()


    def _validate(self):
        # Run all the checks
        self._validate_sub_dirs()
        self._validate_files()

        # Run specific extras
        self._specific_checks()

    def _specfic_checks(self):
        "To be over-ridden in sub-classes."
        raise NotImplementedError()

    def _validate_sub_dirs(self):

        errs = []

        for dr in self._EXPECTED_DIRS:
            if dr not in self._contents:
                errs.append('Required directory "{}" not found in delivery'.format(dr))

        extras = set(self._EXPECTED_DIRS).symmetric_difference(set(self._contents))

        if extras:
            errs.append('Unexpected directories found: {}'.format(str(extras)))

        if errs:
            err_string = '\n' + ', \n'.join(errs)
            raise ParserError('[ERROR] Errors found validating directory: {}:'
                              '{}'.format(self.top_dir, err_string))
          
        print('[INFO] Checked: directory structure.')


    def _validate_files(self):

        errs = []

        for fpath in self._EXPECTED_FILES:
            dr, fname = os.path.split(fpath)
            
            contents = os.listdir(dr)
            

        print('[INFO] Checked file structure (not content yet).')


class SourceAndStationConfigStructureCheck(_StructureCheck):

    _EXPECTED_FILES = [
        'source_configuration/source_configuration_({}+)\.psv'.format(REGEX_SAFE),
        'station_configuration/station_configuration_({}+)\.psv'.format(REGEX_SAFE) ]

class CompleteStructureCheck(_StructureCheck):

    _EXPECTED_DIRS = ['header_table', 'observations_table',
                      'source_configuration', 'station_configuration']
