'''
Created on Feb 28, 2019

@author: William Tucker
'''

from datetime import datetime

from .decorators import row_filter


__all__ = [
    'filter_quality_flag',
    'filter_latitude',
    'filter_longitude',
    'filter_elevation',
    'filter_year',
    'filter_time',
    'filter_temperature',
    'filter_sea_level_pressure',
    'filter_wind_speed',
    'filter_wind_direction',
    'filter_dew_point_temperature',
    'filter_wet_bulb_temperature',
    'filter_relative_humidity',
    'filter_snow_fall',
    'filter_snow_water_equivalent',
    'filter_snow_depth',
    'filter_rainfall',
]


# Maps maximum values (mm) for rainfall against time period
_max_rainfall = {
    0: 0.5,    # Instantaneous
    1: 0.5,    # 2 seconds
    2: 0.5,    # 5 seconds
    3: 0.5,    # 10 seconds
    4: 1,      # 30 seconds
    5: 2,      # 1 minute
    6: 5,      # 2 minutes
    7: 10,     # 5 minutes
    8: 20,     # 10 minutes
    9: 100,    # 1 hour
    10: 250,   # 3 hours
    11: 500,   # 6 hours
    12: 1000,  # 12 hours
    13: 2000,  # 1 day
    14: 2000,  # monthly
}

_max_rainfall_cm = { k: v / 10 for k, v in _max_rainfall.items() }


@row_filter('quality_flag')
def filter_quality_flag(value):
    return value == 0


@row_filter('latitude')
def filter_latitude(value):
    return value >= -90 and value <= 90


@row_filter('longitude')
def filter_longitude(value):
    return value >= -180 and value <= 180


@row_filter('observation_height_above_station_surface')
def filter_elevation(value):
    return value > -432.65 and value < 8850


@row_filter('date_time')
def filter_year(value):
    return value.year > 1650


@row_filter('date_time')
def filter_time(value):
    return value <= datetime.now()


@row_filter('observation_value', 'units')
def filter_temperature(value, units):
    return units == 5 and value >= 200 and value <= 350


@row_filter('observation_value', 'units')
def filter_sea_level_pressure(value, units):
    return units == 32 and value >= 87000 and value <= 109000


@row_filter('observation_value', 'units')
def filter_wind_speed(value, units):
    return units == 731 and value >= 0 and value <= 50


@row_filter('observation_value', 'units')
def filter_wind_direction(value, units):
    return units == 320 and value >= 0 and value <= 359.99999


@row_filter('observation_value', 'units')
def filter_dew_point_temperature(value, units):
    return units == 5 and value >= 200 and value <= 350


@row_filter('observation_value', 'units')
def filter_wet_bulb_temperature(value, units):
    return units == 5 and value >= 200 and value <= 350


@row_filter('observation_value', 'units')
def filter_relative_humidity(value, units):
    return units == 300 and value >= 0 and value <= 100


@row_filter('observation_value', 'units', 'observation_duration')
def filter_snow_fall(value, units, duration):
    return units == 710 and value >= 0 and value <= _max_rainfall[duration]


@row_filter('observation_value', 'units', 'observation_duration')
def filter_snow_water_equivalent(value, units, duration):
    return units == 710 and value >= 0 and value <= _max_rainfall[duration]


@row_filter('observation_value', 'units', 'observation_duration')
def filter_snow_depth(value, units, duration):
    
    # Because units are cm, not mm, we divide max rainfall by 10
    return units == 715 and value >= 0 and value <= _max_rainfall_cm[duration]


@row_filter('observation_value', 'units', 'observation_duration')
def filter_rainfall(value, units, duration):
    return units == 710 and value >= 0 and value <= _max_rainfall[duration]
