import logging
import pickle

from queue import deque


logger = logging.getLogger(__name__)


class ChunkManager:
    """
    Parses data already "chunked" in to Pandas DataFrames and pickled
    to cache files. And allows easy access to chunks.
    """

    def __init__(self, chunks):
        self.all_chunks = chunks
        self.consumed = []
        self.remaining = deque(chunks[:])

    def read_chunks(self):
        
        if len(self.remaining) > 0:
            next_chunk = self.remaining.popleft()
            logger.info('Reading DataFrame from chunk: {}'.format(next_chunk))
            
            with open(next_chunk, 'rb') as reader:
                yield pickle.load(reader)
