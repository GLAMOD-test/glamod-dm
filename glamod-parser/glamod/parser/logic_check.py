
import logging

from glamod.parser.utils import timeit
from glamod.parser.chunk_manager import ChunkManager


logger = logging.getLogger(__name__)


class _LogicCheckBase(object):

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('LogicCheck', '')
        logger.info('Initiating logic checks for: {}'.format(self.ftype))
        self.chunks = sorted(chunks)
        self._count_records()

        self.cm = ChunkManager(self.chunks)

    def _count_records(self):
        "Use the name of the final chunk file to count the records."
        self.record_count = int(self.chunks[-1].split('-')[-1].split('.')[0])
        logger.info('Working on {} records.'.format(self.record_count))

    @timeit
    def run(self):
        raise NotImplementedError



class SourceConfigurationLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        if self.record_count > 10000000:
            raise Exception('TOO MANY RECORDS!!!')

        logger.info('Completed Logic Checks for: {}'.format(self.ftype))
        while 1:
            try:
                self.cm.get_next_chunk()
            except IOError:
                break


class StationConfigurationLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        if self.record_count > 10000000:
            raise Exception('TOO MANY RECORDS!!!')

        logger.info('Completed Logic Checks for: {}'.format(self.ftype))


class HeaderTableLogicCheck(_LogicCheckBase):
    pass


class ObservationsTableLogicCheck(_LogicCheckBase):
    pass

