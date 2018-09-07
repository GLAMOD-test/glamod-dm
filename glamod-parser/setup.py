#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='glamod-parser',
      version='0.4',
      description='GLAMOD CDM data parser',
      author='Ag Stephens',
      author_email='ag.stephens@stfc.ac.uk',
      url='https://github.com/glamod/glamod-dm/glamod-parser',
      packages=find_packages(),
      install_requires =  ['openpyxl', 'psycopg2', 'python-dateutil', 'SQLAlchemy'],
     )
