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

    def pickle_chunks(self, chunks, chunk_name, record_manager=None):
        
        for count, chunk in enumerate(chunks):
            
            if record_manager:
                chunk = record_manager.resolve_data_frame(chunk)
            
            pickle_path = self._get_pickle_path(chunk_name, count, len(chunk))
            self._pickle(chunk, pickle_path)
            
            self._pickled_chunks.append(pickle_path)

    def read_cached_chunks(self):
        
        for pickled_chunk_path in self._pickled_chunks:
            
            logger.info(
                'Reading DataFrame from chunk: {}'.format(pickled_chunk_path)
            )
            with open(pickled_chunk_path, 'rb') as reader:
                yield pickle.load(reader)
    
    def count_records(self):
        """ Use the name of the final chunk file to count the records. """
        
        return int(self._pickled_chunks[-1].split('-')[-1].split('.')[0])
    
    def _pickle(self, chunk, out_path):
        
        logger.info('Pickling chunk to: "{}"'.format(out_path))
        with open(out_path, 'wb') as writer:
            pickle.dump(chunk, writer, protocol=2)
    
    def _get_pickle_path(self, chunk_name, count, this_chunk_length):
        
        zpad = RECORD_COUNT_ZERO_PAD
        _start = count * CHUNK_SIZE + 1 
        _end = _start + this_chunk_length - 1
        fname = f'{chunk_name}.CHUNK.{_start:{zpad}}-{_end:{zpad}}.pickle'
        
        return os.path.join(self._pickle_directory, fname)
