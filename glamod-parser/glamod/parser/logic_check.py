
import logging
import pandas

from pandas import DataFrame

from glamod.parser.utils import timeit
from glamod.parser.filters.generic import match_filter
from glamod.parser.filters.observations_table import *
from collections import namedtuple


logger = logging.getLogger(__name__)


LogicProblem = namedtuple('LogicProblem', ['rows', 'message'])


class _LogicCheckBase(object):

    def __init__(self, chunk_manager):
        self.ftype = self.__class__.__name__.replace('LogicCheck', '')
        logger.info('Initiating logic checks for: {}'.format(self.ftype))
        self._chunk_manager = chunk_manager
        self._count_records()
    
    def _count_records(self):
        "Use the name of the final chunk file to count the records."
        self.record_count = self._chunk_manager.get_record_count()
        logger.info('Working on {} records.'.format(self.record_count))
    
    @staticmethod
    def _apply_filter(data_frame, data_filter, invert=False):
        
        mask = data_frame.apply(data_filter, axis=1)
        filtered_data_frame = data_frame[~mask] if invert else data_frame[mask]
        
        return filtered_data_frame
    
    @classmethod
    def _get_bad_values(cls, data_frame, pre_filter, logic_filter):
        
        if pre_filter:
            data_frame = cls._apply_filter(data_frame, pre_filter)
        
        if not data_frame.empty:
            return cls._apply_filter(data_frame, logic_filter, invert=True)
    
    def _check_data(self, data_frame, truncate=None):
        
        for pre_filter in self._pre_filters:
            data_frame = self._apply_filter(data_frame, pre_filter)
        
        all_rejected_data = DataFrame(columns=data_frame.columns)
        for pre_filter, logic_filter, _ in self._logic_filters:
            
            bad_data = self._get_bad_values(
                data_frame, pre_filter, logic_filter)
            if isinstance(bad_data, DataFrame):
                all_rejected_data = pandas.concat(
                    [all_rejected_data, bad_data])
        
        problem = len(all_rejected_data)
        rejected_sample = all_rejected_data.truncate(after=truncate)
        
        return problem, rejected_sample
    
    def _aggregate_problems(self, data_frame):
        
        if data_frame.empty:
            return []
        
        problems = []
        for pre_filter, logic_filter, filter_columns in self._logic_filters:
            
            problem_rows = []
            bad_data = self._get_bad_values(
                data_frame, pre_filter, logic_filter)
            if isinstance(bad_data, DataFrame):
                for row in bad_data.to_dict('records'):
                    
                    record_id = row[self._id_key]
                    bad_values = [row[key] for key in filter_columns]
                    details = (f'Record {record_id}: Invalid values'
                               f' {bad_values} for columns {filter_columns}')
                    
                    problem_rows.append(details)
            
            if problem_rows:
                problems.append(
                    LogicProblem(problem_rows, logic_filter.__name__))
        
        return problems
    
    @timeit
    def run(self):
        
        logger.info(f'Starting {type(self).__name__}')
        
        all_rejected_samples = None
        total_problem_count = 0
        for chunk in self._chunk_manager.read_cached_chunks():
            problem_count, rejected_sample = self._check_data(chunk)
            total_problem_count += problem_count
            
            if all_rejected_samples == None:
                all_rejected_samples = DataFrame(columns=chunk.columns)
            all_rejected_samples = pandas.concat(
                [all_rejected_samples, rejected_sample])
        
        problems = []
        if isinstance(all_rejected_samples, DataFrame):
            problems = self._aggregate_problems(all_rejected_samples)
        
        logger.info(f'Logic check found {total_problem_count} problems.')
        for problem in problems:
            problem_row_details = '\n'.join(problem.rows)
            logger.warn(f'{problem.message}: \n{problem_row_details}')



class SourceConfigurationLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class StationConfigurationLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class StationConfigurationOptionalLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class HeaderTableLogicCheck(_LogicCheckBase):

    @timeit
    def run(self):
        pass


class ObservationsTableLogicCheck(_LogicCheckBase):

    _id_key = 'observation_id'
    
    _pre_filters = [
        filter_quality_flag,
    ]
    
    _logic_filters = [
        (None, filter_latitude,
            ['latitude']),
        (None, filter_longitude,
            ['longitude']),
        (None, filter_elevation,
            ['observation_height_above_station_surface']),
        (None, filter_year,
            ['date_time']),
        (None, filter_time,
            ['date_time']),
        (match_filter('observed_variable', 85), filter_temperature,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 58), filter_sea_level_pressure,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 107), filter_wind_speed,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 106), filter_wind_direction,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 36), filter_dew_point_temperature,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 41), filter_wet_bulb_temperature,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 38), filter_relative_humidity,
            ['observation_value', 'units']),
        (match_filter('observed_variable', 45), filter_snow_fall,
            ['observation_value', 'units', 'observation_duration']),
        (match_filter('observed_variable', 55), filter_snow_water_equivalent,
            ['observation_value', 'units', 'observation_duration']),
        (match_filter('observed_variable', 53), filter_snow_depth,
            ['observation_value', 'units', 'observation_duration']),
        (match_filter('observed_variable', 44), filter_rainfall,
            ['observation_value', 'units', 'observation_duration']),
    ]

    @timeit
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
