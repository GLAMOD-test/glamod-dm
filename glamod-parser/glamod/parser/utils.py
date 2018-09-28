'''
Created on 28/09/2018

@author: Ag Stephens
'''

import time
import os
import zipfile


from glamod.parser.exceptions import ParserError


def timeit(method):
    "Decorator to wrap functions and time them."
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('[INFO] TIMER: "{}" ran in: {:.5f} seconds'.format(method.__name__, (te - ts)))
        return result
    return timed


def unzip(location, target_dir):
    print('[INFO] Found zip file: {}'.format(location))
    target_dir = os.path.abspath(target_dir)

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    with zipfile.ZipFile(location, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    expected_subdir = os.path.basename(location)[:-4]
    contents = os.listdir(target_dir)

    if contents != [expected_subdir]:
        raise ParserError('[ERROR] Zip file must unzip to directory with identical name '
                          'with ".zip" extension removed. Not: \n{}'.format(str(contents))) 

    print('[INFO] Unzipped contents to: {}'.format(target_dir))
    return os.path.join(target_dir, expected_subdir)

