
import logging

from glamod.parser.utils import timeit


logger = logging.getLogger(__name__)


class _LogicCheckBase(object):

    def __init__(self, chunk_manager):
        self.ftype = self.__class__.__name__.replace('LogicCheck', '')
        logger.info('Initiating logic checks for: {}'.format(self.ftype))
        self._chunk_manager = chunk_manager
        self._count_records()

    def _count_records(self):
        "Use the name of the final chunk file to count the records."
        self.record_count = self._chunk_manager.count_records()
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


class StationConfigurationLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        if self.record_count > 10000000:
            raise Exception('TOO MANY RECORDS!!!')

        logger.info('Completed Logic Checks for: {}'.format(self.ftype))


class StationConfigurationOptionalLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class HeaderTableLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class ObservationsTableLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass
