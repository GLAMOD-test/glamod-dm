"""
Rules for source_configuration files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *

from ._base import OD, _ParserRulesBase


class SourceConfigurationParserRules(_ParserRulesBase):
    
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


    code_table_fields = OD([
        ('product_level', (ProductLevel, 'description', False)),
        ('product_status', (ProductStatus, 'description', False)),
        ('source_format', (SourceFormat, 'format', True)),
        ('data_centre', (Organisation, 'organisation_id', True)),
        ('data_policy_licence', (DataPolicyLicence, 'description', False)),
        ('contact', (Contact, 'contact_id', True)),
        ('contact_role', (Role, 'role', True)),
        ('maintenance_and_update_frequency', (UpdateFrequency, 'frequency', True)),
        ('optional_data', (DataPresent, 'flag', True))
    ])

    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.