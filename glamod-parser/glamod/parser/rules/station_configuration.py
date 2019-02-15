"""
Rules for station_configuration files.
"""

from glamod.parser.convertors import list_of_ints, list_of_strs, \
    int_or_empty, float_or_empty, timestamp_or_empty
from cdmapp.models import IdScheme, SubRegion, Crs, \
    PlatformType, PlatformSubType, Organisation, Contact, Role, StationType, \
    ObservingFrequency, ObservedVariable, DataPresent, \
    CommunicationMethod, AutomationStatus

from ._base import OD, _ParserRulesBase, ForeignKeyLookup, OneToManyLookup


class StationConfigurationParserRules(_ParserRulesBase):

    lookups = [
        ForeignKeyLookup('primary_id_scheme', IdScheme, 'scheme'),
        OneToManyLookup('secondary_id_scheme', IdScheme, 'scheme', resolve_basic=True),
        OneToManyLookup('role', Role, 'role', resolve_basic=True),
        ForeignKeyLookup('station_crs', Crs, 'crs'),
        ForeignKeyLookup('station_type', StationType, 'type'),
        ForeignKeyLookup('platform_type', PlatformType, 'type'),
        ForeignKeyLookup('platform_sub_type', PlatformSubType, 'sub_type'),
        ForeignKeyLookup('operating_institute', Organisation, 'organisation_id'),
        ForeignKeyLookup('operating_territory', SubRegion, 'sub_region'),
        OneToManyLookup('contact', Contact, 'contact_id', resolve_basic=True),
        ForeignKeyLookup('observing_frequency', ObservingFrequency, 'frequency'),
        OneToManyLookup('telecommunication_method', CommunicationMethod, 'method', resolve_basic=True),
        ForeignKeyLookup('station_automation', AutomationStatus, 'automation'),
        OneToManyLookup('observed_variables', ObservedVariable, 'variable', resolve_basic=True),
        ForeignKeyLookup('optional_data', DataPresent, 'flag'),
        
        # Ignore lookups for extended fields
        #ForeignKeyLookup('region', Region, 'region'),
        #ForeignKeyLookup('data_policy_licence', DataPolicyLicence, 'policy'),
        #ForeignKeyLookup('location_method', LocationMethod, 'method'),
        #ForeignKeyLookup('location_quality', LocationQuality, 'quality'),
        #ForeignKeyLookup('sea_level_datum', SeaLevelDatum, 'datum'),
    ]

    fields = OD([

      # Standard fields
        ('primary_id', str),
        ('primary_id_scheme', int_or_empty),
        ('record_number', int),
        ('secondary_id', list_of_strs),
        ('secondary_id_scheme', list_of_ints),
        ('station_name', str),
        ('station_abbreviation', str),
        ('alternative_name', list_of_strs),
        ('station_crs', str),
        ('longitude', float),
        ('latitude', float),
        ('local_gravity', float_or_empty),
        ('start_date', timestamp_or_empty),
        ('end_date', timestamp_or_empty),
        ('station_type', int_or_empty),
        ('platform_type', int_or_empty),
        ('platform_sub_type', int_or_empty),
        ('operating_institute', str),
        ('operating_territory', int_or_empty),
        ('city', str),
        ('contact', list_of_strs),
        ('role', list_of_ints),
        ('observing_frequency', int_or_empty),
        ('reporting_time', list_of_ints),
        ('telecommunication_method', list_of_ints),
        ('station_automation', int_or_empty),
        ('measuring_system_model', list_of_strs),
        ('measuring_system_id', list_of_strs),
        ('observed_variables', list_of_ints),
        ('comment', str),
        ('optional_data', int_or_empty),
        ('bbox_min_longitude', float_or_empty),
        ('bbox_max_longitude', float_or_empty),
        ('bbox_min_latitude', float_or_empty),
        ('bbox_max_latitude', float_or_empty),
        ('metadata_contact', list_of_strs),
        ('metadata_contact_role', list_of_ints),
    ])


    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
        ('region', int_or_empty),
        ('data_policy_licence', int_or_empty),
        ('primary_station_id_scheme', int_or_empty),
        ('location_accuracy', float),
        ('location_method', int_or_empty),
        ('location_quality', int_or_empty),
        ('height_of_station_above_local_ground', float_or_empty),
        ('height_of_station_above_sea_level', float_or_empty),
        ('height_of_station_above_sea_level_accuracy', float_or_empty),
        ('sea_level_datum', float_or_empty),
        ('source_id', str)
    ])

    extended_fields_to_duplicate = ('primary_id', 'record_number')

    index_field = 'primary_id'
