'''
Created on 28/09/2018

@author: Ag Stephens
'''

import time
import os
import zipfile
import logging

logger = None

from glamod.parser.exceptions import ParserError

# Following settings import includes all Django Models
from glamod.parser.settings import *


def _get_logger():
    if logger: return logger

    logger = logging.getLogger(__file__)
    return logger


def log(level, msg):
    """
    Log message `msg` at level `level`.
   
    :param level: level of logging ('INFO', 'ERROR' etc..)
    :param msg: message to log.
    :return: None
    """
    level = level.upper()
    _levels = ['NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL']

    if level not in _levels:
        raise KeyError('Unrecognised log level: {}'.format(level))

    print('[{}] {}'.format(level, msg))


def timeit(method):
    "Decorator to wrap functions and time them."
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        method_name = method.__qualname__
        log('INFO', 'TIMED FUNCTION: "{}" ran in: {:.5f} seconds'.format(method_name, (te - ts)))
        return result
    return timed


def unzip(location, target_dir):
    log('INFO', 'Found zip file: {}'.format(location))
    target_dir = os.path.abspath(target_dir)

    safe_mkdir(target_dir)

    with zipfile.ZipFile(location, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    expected_subdir = os.path.basename(location)[:-4]
    contents = os.listdir(target_dir)

    if contents != [expected_subdir]:
        raise ParserError('[ERROR] Zip file must unzip to directory with identical name '
                          'with ".zip" extension removed. Not: \n{}'.format(str(contents))) 

    log('INFO', 'Unzipped contents to: {}'.format(target_dir))
    return os.path.join(target_dir, expected_subdir)


def report_errors(errs, msg_tmpl):
    err_string = '\n' + ', \n'.join(errs)
    raise ParserError(msg_tmpl.format(err_string))


def count_lines(fpath):
    count = 0

    with open(fpath, 'r', encoding=INPUT_ENCODING) as reader:
        for _ in reader:
            count += 1

    log('INFO', 'File length of "{}" is: {}'.format(fpath, count))
    return count


def map_file_type(lookup, reverse=False):
    """
    Generic mapper for file name to/from table name.

    :param lookup: key to look up (file name or table name).
    :param reverse: direction to do lookup.
    :return: value (looked up in dictionary).
    """
    # Just use the file name (if relevant)
    lookup = os.path.basename(lookup)

    # If lookup key is a class then use its name here
    if not isinstance(lookup, str):
        lookup = lookup.__class__.__name__

    _map = {
        'source_configuration': 'SourceConfiguration',
        'station_configuration': 'StationConfiguration',
        'header_table': 'HeaderTable', 
        'observations_table': 'ObservationsTable'}

    if reverse:
        dct = dict([(_value, _key) for _key, _value in _map.items()])
    else:
        dct = _map

    for _key in dct:
        if lookup.startswith(_key):
            return dct[_key]

    raise KeyError('Cannot lookup mapping for: {}'.format(lookup))


def _field_to_model_mapper(key, reverse=False):
    _map = DB_MAPPINGS
 
    if reverse:
        dct = dict([(_value, _key) for _key, _value in _map.items()])
    else:
        dct = _map
    
    if key not in dct:
        raise KeyError('Cannot lookup mapping for: {}'.format(key))    

    return dct[key]


def field_to_db_model(key):
    return _field_to_model_mapper(key)


def db_model_to_field(key):
    return _field_to_model_mapper(key, reverse=True) 


def get_path_sub_dirs(path, depth=1):
    """
    Returns a sub-directory tree under a path to the depth specified.
    """
    dir_path = os.path.abspath(os.path.dirname(path))
    items = dir_path.strip('/').split('/')

    return '/'.join(items[-(depth):])


def safe_mkdir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)
