import pandas

from glamod.parser.settings import INPUT_ENCODING, INPUT_DELIMITER
from glamod.parser.rules.source_configuration import SourceConfigurationParserRules
from glamod.parser.utils import *

import copy

fpath = 'test_data/glamod_land_delivery_20180928_test002/source_configuration/source_configuration_test002.psv'

fields = copy.deepcopy(SourceConfigurationParserRules.fields)
col_names = [key for key in fields.keys()]

for key in col_names:
    fields[key] = fields[key][0]

use_cols = ['source_id', 'source_format']
df = pandas.read_csv(fpath, encoding=INPUT_ENCODING, delimiter=INPUT_DELIMITER,
                     converters=fields, usecols=use_cols)

for row in df.values[:3]:
    print(row)

print("Testing if they are found in the lookup table...")

def check_lookups_exist_in_code_table(values, indexes, model): 
    assert(len(values)==len(indexes))
    dct = {}
     
    for i in range(len(values)):
        dct.setdefault(values[i], [])
        dct[values[i]].append(indexes[i])

    # Check unique values
    not_found = {}

    for value in set(values):
        if not model.objects.filter(pk=value):
            not_found[value] = dct[value] 

    if not_found:
        print('[ERROR] The following record IDs were not found in table "{}":'.format(
              db_model_to_field(model.__name__)))
        for key in sorted(not_found.keys()):
            print('\tUnmatched ID:  {:8d}; Record indexes: {}'.format(key, not_found[key]))

    return not_found 


check_lookups_exist_in_code_table(df['source_format'], df['source_id'], SourceFormat)
