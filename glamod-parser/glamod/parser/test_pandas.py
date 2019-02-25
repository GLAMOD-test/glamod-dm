import pandas

from glamod.parser.settings import INPUT_DELIMITER
from glamod.parser.rules.source_configuration import SourceConfigurationParserRules
from glamod.parser.utils import *

from cdmapp.models import SourceFormat, ProductLevel

import copy

import numpy as numpy

fpath = 'test_data/glamod_land_delivery_20180928_test002/source_configuration/source_configuration_test002.psv'

fields = copy.deepcopy(SourceConfigurationParserRules.fields)
col_names = [key for key in fields.keys()]

for key in col_names:
    fields[key] = fields[key][0]

na_values = {'product_level': 'NULL'}


use_cols = ['source_id', 'source_format', 'product_level']
df = pandas.read_csv(fpath, encoding=INPUT_ENCODING, delimiter=INPUT_DELIMITER,
                     converters=fields, usecols=use_cols)

for row in df.values[:7]:
    print(row)

print(fields)
print("Testing if they are found in the lookup table...")


class ABC(object):
    def __init__(self): pass

    def _run_batch_lookups_of_code_tables(self):
        pass 

    def _check_lookups_exist_in_code_table(self, values, indexes, model): 
        assert(len(values)==len(indexes))
        dct = {}
     
        for i in range(len(values)):
            value = values[i]
            if is_null(value): continue
            
            dct.setdefault(value, [])
            dct[value].append(indexes[i])

        # Check each value only once and record those not found
        not_found = {}

        for value in sorted(list(set(dct.keys()))):
            if not model.objects.filter(pk=value):
                not_found[value] = dct[value] 

        if not_found:
            print('[ERROR] The following record IDs were not found in table "{}"')
            for key in sorted(not_found.keys()):
                print('\tUnmatched ID:  {:8d}; Record indexes: {}'.format(key, not_found[key]))

        return not_found 


abc = ABC()

print(type(df['product_level'][0]))
to_check = [
    (df['source_format'], df['source_id'], SourceFormat),
    (df['product_level'], df['source_id'], ProductLevel),
]

for values, indexes, cls in to_check:
    abc._check_lookups_exist_in_code_table(values, indexes, cls)






