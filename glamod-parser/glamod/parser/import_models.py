import os
import sys
sys.path.append('../../../../glamod-django-apps/glamod-cdm-browser/glamod_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_site.settings'

import django
django.setup()

print("Importing models...")
from cdmapp.models import *
from cdmapp.models import _ALL_MODELS

for _model in _ALL_MODELS.keys():
    print(_model)

x = HeaderTable.objects.first()
print(x)

a = x._meta.get_fields()
b = a[0]

o = ObservationsTable.objects.get(pk='0-20000-0-72208-1-1963-06-05-44-13')
# header_tables/0-20000-0-72406-1-1987-04-07/
o = HeaderTable.objects.get(pk='0-20000-0-72406-1-1987-04-07')
