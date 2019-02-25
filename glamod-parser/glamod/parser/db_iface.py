"""
db_iface.py
===========

Interface to the DB - managed through the django ORM.

"""



from cdmapp.models import SourceConfiguration

first = SourceConfiguration.objects.first()

