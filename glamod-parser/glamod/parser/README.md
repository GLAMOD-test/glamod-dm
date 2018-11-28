# Structure and usage of the GLAMOD parser

## Overview

The GLAMOD parser is a tool that can read input data files, check various aspects 
of them and then load the content into the "CDM" (Common Data Model) database. 

The parser works in two modes:

 1. Parse inventory-level information (using the *Source/Station Processor*):
   - Source Configuration files (info about data sources)
   - Station Configuration files (info about stations)

 2. Parse observation data (using the *Header/Observations Processor*):
   - Header Table files (common info for a set of observations)
   - Observations Table files (the actual measurement values/details)
   
Each of the processors follows a similar workflow:

 1. Run Structure checks:
   - directory and file names
   - existence of directories and files
   
 2. Run Content checks:
   - read each file
   - check column names
   - run lookups of values where they should exist in code tables
   - read file and cache content in *chunk files* (as `pandas.DataFrame` instances)
   
 3. Run Logic checks:
   - read the *chunk files*
   - values for certain columns must conform to certain rules
   - for some columns only a fixed percentage can exceed a certain threshold
   
 4. Write to DB:
   - read the *chunk files*
   - apply rules to get content from lookups and extended DB in order to populate all
     required columns
   - write content to relevant DB tables
   
## The rules of the parser and processors

There are a number of specific rules that define the required content for each file
type. These rules live in:

```
rules/source_configuration.py
rules/station_configuration.py

rules/header_table.py
rules/observations_table.py
```

Each of these files contains a class that defines the rules. Each class has some or
all of the following attributes, used to define how the parser should read and use
the data in the input files:

 - `.fields` (OrderedDict): standard fields that will exist as column headers and map 
   directly to the CDM.
 - `.extended_fields` (OrderedDict): these fields are not defined in the CDM table schema.
   Instead, they are included here so that they can be looked up when loading data for other
   tables. This is an efficiency gain because the values here will be broadcast to all 
   records in the other tables. This data is stored in the secondary database as part of the
   `deliveries` app.
 - `.extended_fields_to_duplicate` (List): these fields will be *both* stored in the 
   `deliveries` DB but will also be saved to the CDM DB table.
 - `.index_field` (String): indicates the primary key field.
 - `.code_table_fields` (OrderedDict): a selection of fields with their mappings to a specific 
   Code Table and the lookup key (i.e. column) within that table.
 - `.vlookup_fields` (OrderedDict): fields that need to be looked up in other tables in order
   to be populated. For example, a number of fields remain constant within a Header Table so 
   we use a lookup to the Station Configuration/extended tables in order to get these values.
   The values are therefore not included in the input files even though the data is required
   in the CDM DB.

## Pre-requisites

You will need to set up the following for the parser to work.

### Set up the environment

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

## Running the parser

Here are some examples of running the parser with test data.

### Parsing the Source/Station Configuration files

To run the parser on a directory containing Source and Station Configuration files:

```
python parse.py -t source test_data/glamod_land_delivery_20180928_source-v6.2
```

### Parsing the Header and Observations Table files

To run the parser on a directory containing Header and Observations Table files:

```
python parse.py -t data test_data/glamod_land_delivery_20180928_data-v6.2
```


### OLD - needs a rewrite - A Data Delivery Package (DDP)

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

Need to reference the `source_configuration` and `station_configuration` records via the primary keys (so those records will need to have been pre-loaded).

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

