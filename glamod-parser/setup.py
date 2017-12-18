#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='glamod-parser',
      version='0.3',
      description='GLAMOD CDM data parser',
      author='William Tucker',
      author_email='william.tucker@stfc.ac.uk',
      url='https://github.com/glamod/glamod-dm/glamod-parser',
      packages=find_packages(),
      install_requires =  ['openpyxl', 'psycopg2', 'python-dateutil', 'SQLAlchemy'],
     )