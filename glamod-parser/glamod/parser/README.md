# Structure and usage of the GLAMOD parser

## Pre-requisites

You will need to set up the following for the parser to work.

### 1. Set up the environment

Set up a Python3.6 conda or virtual environment and install dependencies, e.g.:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Ensure the app can talk to the CDM-Browser Django app, e.g.:

In `python`, try running:


```
import os
import sys
sys.path.append('../../../../glamod-django-apps/glamod-cdm-browser/glamod_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_site.settings'

import django
django.setup()

print("Importing models...")
from cdmapp.models import *

print(HeaderTable.objects.count()
```

### 3. A Data Delivery Package (DDP)

This section outlines the required structure for each data delivery package (DDP).

Note that there is a `<specifier>` component in the top-level directory and the 
file names that ties together different files. It is acceptable for a data provider
to generate separate DDPs that refer to the same `<specifier>`. For example, the 
Source Configuration and Station Configuration components might be delivered in 
an initial DDP and the actual data (Header Table and Observation Table) could be 
sent later. The `<specifier>` would be used by both the provider and recipient in 
order to identify the connection between the DDPs.

 1. The top-level directory should be named:
   `glamod_<domain>_delivery_<YYYY-MM-DD>_<specifier>/`
   - where `<domain>` is either "land" or "marine"
   - and `<specifier>` is a string that can be defined as required by the provider.
   - Note that the the top-level directory can be zipped up with a `.zip` extension.

 2. Sub-directories:
   - There should be a number of sub-directories as specified here:
     i. `source_configuration/` - containing:
       - 1 x `source_configuration_<specifier>.psv`
     ii. `station_configuration/` - containing: 
       - 1 x `station_configuration_<specifier>.psv`
     iii. `header_table/` - containing:
       - N x `header_table_<specifier>_<label>.psv`
     iv. `observations_table/` - containing: 
       - N x `observations_table_<specifier>_<label>.psv`

     Notes on the sub-directories:
       - There must be only one `source_configuration` and `station_configuration` file.
       - There must be the same number of `header_table` and `observations_table` files.
       - The latter tables include a suffix of `_<label>` which is used to distinguish
         between each of the files. 
       - The rows in the `header_table` and `observations_table` files must be paired.
       - Sub-directories can be zipped up with a `.zip` extension.

## How to use the parser


## How the parser works

### High-level overview

Need to reference the `source_configuration` and `station_configuration` records via the 
primary keys (so those records will need to have been pre-loaded).

- walk the structure and check everything is named correctly
  - if zipped then interrogate the zip structure without unzipping

- assert number of files are correct for each type

- Parse source conf and station conf
 - do mappings
 - do checks
 - if all good:
  - per record: check if already in db, if not load into db
  - log all

- Parse pairs of header and obs files:
 - look up relevant files (***or records***) in source conf & station conf
 - do mappings
 - do checks
 - if all good:
  - per record: check if already in db, if not load into db
  - log all

- Provide a report of how it went

### Parsing individual records

The generic approach to parsing a `.psv` file is as simple as:

 1. Load the rules for a given file type.
 2. Read the header row
 3. For each record (row):
  - check content:
   - data types
   - mappings
   - lookups to other tables/files
   - default values
  - completeness check
  - cross-check with other file(s) as required:
   - e.g. header table and observation table - should have same number of rows 
  - save/cache the result (without yet writing to DB)

## Representing the rules in code

For each field (in each table) we need to know:

 1. is mandatory?
 2. is default defined?
 3. is null allowed?
 4. is lookup check required - in real DB table?
 5. what is correct type?
 6. does provided type match correct type?
 7. is there a specific rule for this type?

Logical solution:

 - each field is a class instance or a NamedTuple instance, with properties:
  - data_type:     use primitive and bespoke types as required
  - default:       as defined by `data_type`
  - is_required:   boolean  
  - lookup_ref:    string as: '<table_name>.<prop_name>' 
  - copy_to:        list: ['<table_name>.<prop_name>', '<table_name>.<prop_name>', ...] 

????
  - complex_lookups???:  HOW TO CHECK ON CROSS-LOOKUPS WITH OTHER FIELDS?
    1. In single fields?
    2. Or, define them as separate secondary rules defined separately, so you have:
      i.  _FIELD_RULES
      ii. _COMBINATION_RULES
????

Notes:

 1. `data_type` might be defined as a new class with validation rules included.
