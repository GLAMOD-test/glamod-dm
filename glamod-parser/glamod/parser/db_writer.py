import copy

from glamod.parser.settings import *
from glamod.parser.utils import log, timeit
from glamod.parser.chunk_manager import ChunkManager

from glamod.parser.rules import (SourceConfigurationParserRules,
    StationConfigurationParserRules)


class _DBWriterBase(object):

    app_model = None
    rules = None

    def __init__(self, chunks):
        self.ftype = self.__class__.__name__.replace('DBWriter', '')
        log('INFO', 'Initiating DB Writer for: {}'.format(self.ftype))

        self.chunks = sorted(chunks)
        self.cm = ChunkManager(self.chunks)

    @timeit
    def write_to_db(self):
        log('INFO', 'Completed Logic Checks for: {}'.format(self.ftype))
        while 1:
            try:
                df = self.cm.get_next_chunk()
                self._write_chunk(df)
            except IOError:
                break

    def _write_chunk(self, df):
        raise NotImplementedError


class SourceConfigurationDBWriter(_DBWriterBase):

    app_model = SourceConfiguration
    rules = SourceConfigurationParserRules()

    def _write_chunk(self, df):

        for count, record in enumerate(df.to_dict('records')):
            print(f'Writing record: {count + 1:5d}')

            self._write_record(record)


    def _write_record(self, record):
        # Deal with foreign key components in the record first
        rec = copy.deepcopy(record)

        for fk_field, (fk_model, fk_arg, is_primary_key) in self.rules.foreign_key_fields_to_add.items():
            if rec[fk_field] == INT_NAN and is_primary_key:
                log('DEBUG', f'Ignoring NAN field for: {fk_field}')
                del rec[fk_field]
                continue

            log('WARN', 'Could CHANGE MODEL TO USE `models.AutoField()` but not tampering (yet)!')
            if is_primary_key:
                kwargs = {'pk': rec[fk_field]}
            else:
                pk = fk_model.objects.count()
                kwargs = {'pk': pk, fk_arg: rec[fk_field]}

            fk_obj, created = fk_model.objects.get_or_create(**kwargs)
            if created:
                log('INFO', 'Created foreign key record: {}'.format(fk_obj))

            rec[fk_field] = fk_obj

        try:
            _, created = self.app_model.objects.get_or_create(**rec)
        except Exception as err:
            import pdb; pdb.set_trace()
            print(str(rec))
            raise Exception(err)


        print('Was it created? {}'.format(str(created)))

class StationConfigurationDBWriter(_DBWriterBase):

    app_model = StationConfiguration
    rules = StationConfigurationParserRules()

    def _write_chunk(self, df):
        raise NotImplementedError
        for record in df.to_dict('records'):
            print(record)



class HeaderTableDBWriter(_DBWriterBase):
    pass


class ObservationsTableDBWriter(_DBWriterBase):
    pass