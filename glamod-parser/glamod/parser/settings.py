import os
import sys

sys.path.append('../../../../glamod-django-apps/glamod-cdm-browser/glamod_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_site.settings'

import django
django.setup()

print("[INFO] Importing django models for db checks...")
from cdmapp.models import *


REGEX_SAFE = '[a-zA-Z0-9-]'
INPUT_ENCODING = 'windows-1252'
