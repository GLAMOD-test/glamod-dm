

from glamod.parser.utils import log, timeit
from glamod.parser.chunk_manager import ChunkManager


class _DBWriterBase(object):

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('DBWriter', '')
        log('INFO', 'Initiating DB Writer for: {}'.format(self.ftype))

        self.chunks = sorted(chunks)
        self.cm = ChunkManager(self.chunks)


    def write_to_db(self):
        log('INFO', 'Writing data to DB')

class SourceConfigurationDBWriter(_DBWriterBase):
    pass


class StationConfigurationDBWriter(_DBWriterBase):
    pass


class HeaderTableDBWriter(_DBWriterBase):
    pass


class ObservationsTableDBWriter(_DBWriterBase):
    pass