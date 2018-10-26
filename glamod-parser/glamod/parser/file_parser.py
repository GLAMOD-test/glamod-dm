'''
Created on 01 Oct 2018

@author: Ag Stephens
'''

import os
import pickle

import pandas

from glamod.parser.exceptions import ParserError
from glamod.parser.utils import get_path_sub_dirs, safe_mkdir
from glamod.parser.settings import (INPUT_ENCODING, INPUT_DELIMITER, 
    VERBOSE_LOGGING, CHUNK_SIZE, RECORD_COUNT_ZERO_PAD, CHUNK_CACHE_DIR_DEPTH,
    CHUNK_CACHE_DIR)


class FileParser(object):
    
    def __init__(self, fpath, delimiter=INPUT_DELIMITER, encoding=INPUT_ENCODING):
        self.fpath = fpath 
        self.delimiter = delimiter
        self.encoding = encoding
 
        self.data_dirs = get_path_sub_dirs(fpath, depth=CHUNK_CACHE_DIR_DEPTH)
        self.chunk_cache_target_dir = os.path.join(CHUNK_CACHE_DIR, self.data_dirs)

        self._fh = open(fpath, 'r', encoding=self.encoding)
        self._col_names = self._parse_header()
        self.chunks = []


    def rewind(self, to_line=0):
        "Sets the seek position at the start of the file."
        self._fh.seek(0)

        if to_line > 0:
            for _ in range(to_line): 
                self._fh.readline() 


    def _parse_header(self):
        assert(self._fh.tell() == 0)
        return self.readline()


    def readline(self):
        "Reads next line and splits on delimiter."
        return [_.strip() for _ in self._fh.readline().rstrip().split(self.delimiter)]         


    def get_column_names(self):
        return self._col_names


    def get_subset_dataframe(self, convertors=None, columns=None):
        self.rewind()
        df = pandas.read_csv(self._fh, encoding=self.encoding, 
                             delimiter=self.delimiter,
                             converters=convertors, usecols=columns,
                             skipinitialspace=True, verbose=VERBOSE_LOGGING)
        return df


    def _get_chunk_file_path(self, count, this_chunk_length):
        # Ensure cache directory is ready
        target_dir = self.chunk_cache_target_dir
        safe_mkdir(target_dir)

        base_name = os.path.splitext(os.path.basename(self.fpath))[0]
        zpad = RECORD_COUNT_ZERO_PAD

        _start = count * CHUNK_SIZE + 1 
        _end = _start + this_chunk_length - 1
        fname = f'{base_name}.CHUNK.{_start:{zpad}}-{_end:{zpad}}.pickle'

        return os.path.join(target_dir, fname)

    
    def read_and_pickle_chunks(self, convertors=None):
        if self.chunks:
            raise Exception('[ERROR] Chunks have already been pickled for: "{}"'.format(self.fpath))

        self.rewind()
        _chunk_reader = pandas.read_csv(self._fh, encoding=self.encoding,
                             delimiter=self.delimiter,
                             converters=convertors, skipinitialspace=True, 
                             verbose=VERBOSE_LOGGING, chunksize=CHUNK_SIZE)

        # Loop through chunks, converting to dicts and writing to cache
        for counter, df in enumerate(_chunk_reader):

            print('[DEBUG] Chunking as DataFrame, but "to_dict(\'records\')" also allowed...?')
            out_path = self._get_chunk_file_path(counter, len(df))
            self.chunks.append(out_path)

            print('[INFO] Pickling chunk to: "{}"'.format(out_path))
            with open(out_path, 'wb') as writer:
                pickle.dump(df, writer, protocol=2)

        print('[INFO] All chunks written for: "{}"'.format(self.fpath))


    def close(self):
        self._fh.close()

