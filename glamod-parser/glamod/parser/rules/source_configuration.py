"""
Rules for source_configuration files.
"""

from glamod.parser.convertors import list_of_ints, list_of_strs, \
    int_or_empty, float_or_empty, timestamp_or_empty
from cdmapp.models import ProductLevel, ProductStatus, SourceFormat, \
    Organisation, DataPolicyLicence, Contact, Role, UpdateFrequency, \
    DataPresent

from ._base import OD, _ParserRulesBase, ForeignKeyLookup, OneToManyLookup


class SourceConfigurationParserRules(_ParserRulesBase):
    
    lookups = [
        ForeignKeyLookup('product_level', ProductLevel, 'description'),
        ForeignKeyLookup('product_status', ProductStatus, 'description'),
        ForeignKeyLookup('source_format', SourceFormat, 'format'),
        ForeignKeyLookup('data_centre', Organisation, 'organisation_id'),
        ForeignKeyLookup('data_policy_licence', DataPolicyLicence, 'policy'),
        OneToManyLookup('contact', Contact, 'contact_id', resolve_basic=True),
        OneToManyLookup('contact_role', Role, 'role', resolve_basic=True),
        ForeignKeyLookup('maintenance_and_update_frequency', UpdateFrequency, 'frequency'),
        ForeignKeyLookup('optional_data', DataPresent, 'flag'),
    ]
    
    fields = OD([
        ('source_id', str),
        ('product_id', None),
        ('product_name', str),
        ('product_code', str),
        ('product_version', str),
        ('product_level', int_or_empty),
        ('product_uri', str),
        ('description', str),
        ('product_references', list_of_strs),
        ('product_citation', list_of_strs),
        ('product_status', str),
        ('source_format', int_or_empty),
        ('source_format_version', str),
        ('source_file', str),
        ('source_file_checksum', str),
        ('data_centre', str),
        ('data_centre_url', str),
        ('data_policy_licence', str),
        ('contact', list_of_strs),
        ('contact_role', list_of_ints),
        ('history', str),
        ('comments', str),
        ('timestamp', timestamp_or_empty),
        ('maintenance_and_update_frequency', int_or_empty),
        ('optional_data', int_or_empty),
        ('bbox_min_longitude', float_or_empty),
        ('bbox_max_longitude', float_or_empty),
        ('bbox_min_latitude', float_or_empty),
        ('bbox_max_latitude', float_or_empty),
        ('metadata_contact', list_of_strs),
        ('metadata_contact_role', list_of_ints),
    ])

    index_field = 'source_id'
