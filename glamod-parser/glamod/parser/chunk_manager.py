import os
import logging
import pickle

from glamod.parser.utils import safe_mkdir
from glamod.parser.settings import CHUNK_SIZE, RECORD_COUNT_ZERO_PAD


logger = logging.getLogger(__name__)


class ChunkManager:
    """
    Parses data already "chunked" in to Pandas DataFrames and pickled
    to cache files. And allows easy access to chunks.
    """

    def __init__(self, pickle_directory):
        
        safe_mkdir(pickle_directory)
        self._pickle_directory = pickle_directory
        self._pickled_chunks = []
        
        self._record_count = 0

    def pickle_chunks(self, chunks, chunk_name, record_manager=None):
        
        for count, chunk in enumerate(chunks):
            
            chunk_length = len(chunk)
            pickle_path = self._get_pickle_path(chunk_name, count, chunk_length)
            
            if not os.path.exists(pickle_path) and record_manager:
                
                chunk = record_manager.resolve_data_frame(chunk)
                self._pickle(chunk, pickle_path)
            
            else:
                logger.info(
                    f'Skipping check for pre-pickled chunk: {pickle_path}.')
            
            self._pickled_chunks.append(pickle_path)
            self._record_count += chunk_length

    def read_cached_chunks(self):
        
        for pickled_chunk_path in self._pickled_chunks:
            
            if not os.path.isfile(pickled_chunk_path):
                logger.error(f'Pickle file not found: {pickled_chunk_path}')
                continue
            
            logger.info(
                'Reading DataFrame from chunk: {}'.format(pickled_chunk_path)
            )
            with open(pickled_chunk_path, 'rb') as reader:
                yield pickle.load(reader)
    
    def get_record_count(self):
        """ Use the name of the final chunk file to count the records. """
        
        return self._record_count
    
    def _pickle(self, chunk, out_path):
        
        logger.info('Pickling chunk to: "{}"'.format(out_path))
        with open(out_path, 'wb') as writer:
            pickle.dump(chunk, writer, protocol=2)
    
    def _get_pickle_path(self, chunk_name, count, chunk_length):
        
        zpad = RECORD_COUNT_ZERO_PAD
        _start = count * CHUNK_SIZE + 1 
        _end = _start + chunk_length - 1
        fname = f'{chunk_name}.CHUNK.{_start:{zpad}}-{_end:{zpad}}.pickle'
        
        return os.path.join(self._pickle_directory, fname)
