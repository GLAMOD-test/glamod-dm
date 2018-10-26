"""
Plan for generic content check:

1. Check column names are correct
2. In rules, define an instance of FieldCheck
3. Parse each record and cycle through FieldCheck instances

"""

import copy

from glamod.parser.settings import INPUT_ENCODING, INPUT_DELIMITER, INT_NAN
from glamod.parser.utils import log, db_model_to_field
from glamod.parser.file_parser import FileParser
from glamod.parser.rules import (
     SourceConfigurationParserRules, StationConfigurationParserRules )


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

        # Now read the data in and cache chunks on the file system
        self._read_and_cache_chunks()


    def _check_column_names(self):
        expected = [key for key in self._rules.expected_fields.keys()]
        actual = self._parser.get_column_names()

        if expected != actual:
            diff = list(set(expected).symmetric_difference(actual)) 
            raise Exception('Column names are incorrect in file: {}'
                            '\n\n\tShould be: {}\n\n\tThe DIFFERENCE was '
                            'identified as: {}'.format(
                            self.fpath, expected, diff))


    def _run_batch_lookups_of_code_tables(self):
        fields = copy.deepcopy(self._rules.fields)         
        col_names = [key for key in fields.keys()]

        for key in col_names:
            fields[key] = fields[key][0]

        index_field = self._rules.index_field
        code_table_fields_dct = self._rules.code_table_fields

        columns = [index_field] + [_key for _key in code_table_fields_dct.keys()]

        # Cache a DataFrame with all required columns
        df = self._parser.get_subset_dataframe(convertors=fields, columns=columns)

        for lookup_col, _model in code_table_fields_dct.items():

            log('INFO', 'Checking column "{}" in: {}'.format(lookup_col, self.fpath))
            self._check_lookups_exist_in_code_table(df[lookup_col], df[index_field],
                                                    _model)
        

    def _check_lookups_exist_in_code_table(self, values, indexes, model):
        assert(len(values)==len(indexes))
        dct = {}

        for i in range(len(values)):
            value = values[i]
            if value == INT_NAN: continue

            # Treat a list of values separately - need to separate them individually
            if type(value) is list:
                for item in value:
                    dct.setdefault(item, [])
                    dct[item].append(indexes[i])
            # or simple case where value is just a value
            else:
                dct.setdefault(value, [])
                dct[value].append(indexes[i])

        # Check each value only once and record those not found
        not_found = {}

        for value in sorted(list(set(dct.keys()))):
            try:
                _check = model.objects.filter(pk=value)
            except:
                log('ERROR', 'Could not lookup value "{}" in code table, so IGNORING check.'
                             .format(value))
                continue

            if not _check:
                not_found[value] = dct[value]

        if not_found:
            log('ERROR', 'The following record IDs were not found in table "{}":'.format(
                  db_model_to_field(model.__name__)))

            for key in sorted(not_found.keys()):
                if type(key) == int: 
                    format = '{:8d}'
                else:
                    format = '{}'

                _tmpl = '[ERROR]\tUnmatched ID:  ' + format + '; Record indexes: {}'
                print(_tmpl.format(key, not_found[key]))

        return not_found


    def _read_and_cache_chunks(self):
        conv_funcs = {}

        for key in self._rules.fields.keys():
            conv_funcs[key] = self._rules.fields[key][0]

        # Read in and cache the data as pickled chunks
        self._parser.read_and_pickle_chunks(convertors=conv_funcs)
        self.chunks = self._parser.chunks


class SourceConfigurationContentCheck(_ContentCheck):

    _rules = SourceConfigurationParserRules()

    def run(self): 
        super(SourceConfigurationContentCheck, self).run()
        log('INFO', 'Completed {} on: {}'.format(self._cls, self.fpath))


class StationConfigurationContentCheck(_ContentCheck):

    _rules = StationConfigurationParserRules()

    def run(self):
        super(StationConfigurationContentCheck, self).run()
        log('INFO', 'Completed {} on: {}'.format(self._cls, self.fpath))
