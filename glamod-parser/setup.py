#!/usr/bin/env python

from distutils.core import setup

setup(name='glamod-parser',
      version='0.2',
      description='GLAMOD CDM data parser',
      author='William Tucker',
      author_email='william.tucker@stfc.ac.uk',
      url='https://github.com/glamod/glamod-dm/glamod-parser',
      packages=['db', 'parse'],
      install_requires =  ['openpyxl', 'psycopg2', 'python-dateutil', 'SQLAlchemy'],
     )