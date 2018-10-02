"""
Plan for generic content check:

1. Check column names are correct
2. In rules, define an instance of FieldCheck
3. Parse each record and cycle through FieldCheck instances

"""


from glamod.parser.utils import log
from glamod.parser.file_parser import FileParser
from glamod.parser.rules import (
     SourceConfigurationParserRules, StationConfigurationParserRules )
#from glamod.parser.field_check import FieldCheck



class _ContentCheck(object):

    _rules = None

    def __init__(self, fpath):
        self.fpath = fpath
        self._cls = self.__class__.__name__


    def run(self):
        log('INFO', 'Starting {} on: {}'.format(self._cls, self.fpath))
        self._parser = FileParser(self.fpath)
       
        # Check column names are correct
        self._check_column_names()

        # Run lookups to code tables first
        self._run_batch_lookups_of_code_tables()


    def _check_column_names(self):
        expected = [key for key in self._rules.fields.keys()]
        actual = self._parser.get_column_names()

        if expected != actual:
            diff = list(set(expected).symmetric_difference(actual)) 
            raise Exception('Column names are incorrect in file: {}'
                            '\n\n\tShould be: {}\n\n\tThe DIFFERENCE was '
                            'identified as: {}'.format(
                            self.fpath, expected, diff))


    def _run_batch_lookups_of_code_tables(self):
        pass          


class SourceConfigurationContentCheck(_ContentCheck):

    _rules = SourceConfigurationParserRules

    def run(self): 
        super(SourceConfigurationContentCheck, self).run()
        log('INFO', 'Completed {} on: {}'.format(self._cls, self.fpath))

class StationConfigurationContentCheck(_ContentCheck):

    _rules = StationConfigurationParserRules    

    def run(self):
        super(StationConfigurationContentCheck, self).run()
