
import pickle
from queue import deque


from glamod.parser.utils import log


class ChunkManager(object):
    """
    Parses data already "chunked" in to Pandas DataFrames and pickled
    to cache files. And allows easy access to chunks.
    """

    def __init__(self, chunks):
        self.all_chunks = chunks
        self.consumed = []
        self.remaining = deque(chunks[:])

    def get_next_chunk(self):
        if len(self.remaining) == 0:
            raise IOError('All chunks already read!')

        next_chunk = self.remaining.popleft()
        log('DEBUG', 'Reading DataFrame from chunk: {}'.format(next_chunk))

        with open(next_chunk, 'rb') as reader:
            return pickle.load(reader)


