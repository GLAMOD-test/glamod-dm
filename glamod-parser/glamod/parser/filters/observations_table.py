'''
Created on Feb 28, 2019

@author: William Tucker
'''

from datetime import datetime

from .base import row_filter


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
    return units == 710 # TODO: implement the rest


@row_filter('observation_value', 'units', 'observation_duration')
def filter_snow_water_equivalent(value, units, duration):
    return units == 710 # TODO: implement the rest


@row_filter('observation_value', 'units', 'observation_duration')
def filter_snow_depth(value, units, duration):
    return units == 715 # TODO: implement the rest


@row_filter('observation_value', 'units', 'observation_duration')
def filter_rainfall(value, units, duration):
    return units == 710 # TODO: implement the rest
