import os
import sys
import re

sys.path.append('../../../../glamod-django-apps/glamod-cdm-browser/glamod_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_site.settings'

import django
django.setup()

print("[INFO] Importing django models for db checks...")
from cdmapp.models import *
from cdmapp.models import _ALL_MODELS

from deliveries_app.models import *

REGEX_SAFE = '[a-zA-Z0-9-.]'

INPUT_DELIMITER = '|'
INPUT_ENCODING = 'windows-1252'

DB_MAPPINGS = dict([(re.sub('s$', '', _value), _key) for _key, _value in _ALL_MODELS.items()])

INT_NAN = -9999

VERBOSE_LOGGING = False

CHUNK_SIZE = 25
RECORD_COUNT_ZERO_PAD = '07d' # 10 million records limit expected
CHUNK_CACHE_DIR = './chunk-cache'
CHUNK_CACHE_DIR_DEPTH = 2
