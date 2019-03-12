
import os
import re
import logging


from .utils import count_lines
from .exceptions import ParserError
from .settings import REGEX_SAFE, HEADER_FILE_LOCATION, HEADER_FILE_REGEX, \
    OBSERVATIONS_FILE_LOCATION, OBSERVATIONS_FILE_REGEX, FILE_LIMIT


logger = logging.getLogger(__name__)


class _StructureCheckBase:
    
    def __init__(self, top_directory):
        
        self._file_directories = [os.path.join(top_directory, directory) \
            for directory in self.expected_directories]
        self._found_files = []
    
    def run(self):
        self._validate()
    
    def get_files(self):
        return self._found_files
    
    def _validate(self):
        
        # Run all the checks
        self._validate_sub_dirs()
        self._validate_file_existence()
        
        # Run specific checks
        self._specific_checks()
    
    def _validate_sub_dirs(self):
        pass
    
    def _validate_file_existence(self):
        
        match = re.compile(self.file_name_pattern)
        
        for directory in self._file_directories:
            for file_name in os.listdir(directory):
                if match.match(os.path.basename(file_name)):
                    
                    file_path = os.path.join(directory, file_name)
                    self._found_files.append(file_path)
        
        if not self._found_files:
            logger.error(
                f'No files found at {self._file_directories} '
                f'with pattern: {self.file_name_pattern}'
            )
        else:
            
            file_count = len(self._found_files)
            logger.info(f'Found a total of {file_count} files.')
            if FILE_LIMIT and FILE_LIMIT < file_count:
                
                logger.info(f'Loading only the first {FILE_LIMIT} files.')
                self._found_files = sorted(self._found_files)[:FILE_LIMIT]
        
        logger.info('Checked file structure (not content yet).')
    
    def _specific_checks(self):
        """ To be over-ridden in sub-classes. """
        raise NotImplementedError()


class SourceAndStationConfigStructureCheck(_StructureCheckBase):
    
    def _specific_checks(self):
        pass


class HeaderAndObservationsTablesStructureCheck(_StructureCheckBase):
    
    def _specific_checks(self):
        pass
        
        # TODO: find a way to reproduce this check elsewhere
        #self._validate_file_lengths()
    
    def _validate_file_lengths(self):
        """ Check that all header and observation tables have equal number of
        records.
        """
        
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


class HeaderTableStructureCheck(
        HeaderAndObservationsTablesStructureCheck):
    
    expected_directories = [HEADER_FILE_LOCATION]
    file_name_pattern = \
        HEADER_FILE_REGEX


class ObservationsTableStructureCheck(
        HeaderAndObservationsTablesStructureCheck):
    
    expected_directories = [OBSERVATIONS_FILE_LOCATION]
    file_name_pattern = \
        OBSERVATIONS_FILE_REGEX


class SourceConfigurationStructureCheck(
        SourceAndStationConfigStructureCheck):
    
    expected_directories = ['source_configuration']
    file_name_pattern = \
        'source_configuration_({}+)\.psv'.format(REGEX_SAFE)


class StationConfigurationStructureCheck(
        SourceAndStationConfigStructureCheck):
    
    expected_directories = ['station_configuration']
    file_name_pattern = \
        'station_configuration_(?!optional)({}+)\.psv'.format(REGEX_SAFE)


class StationConfigurationOptionalStructureCheck(
        SourceAndStationConfigStructureCheck):
    
    expected_directories = ['station_configuration_optional']
    file_name_pattern = \
        'station_configuration_optional_({}+)\.psv'.format(REGEX_SAFE)
