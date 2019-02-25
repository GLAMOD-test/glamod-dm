from cdmapp.models import Contact, ProductLevel, ProductStatus, SourceFormat, \
    Organisation, DataPolicyLicence, Role, UpdateFrequency, DataPresent, \
    SourceConfiguration

"""
Fixes:

product_id: nan to ''
source_format: to SourceFormat instance OR None
maintenance_and_update_frequency: -9999 TO UpdateFrequency instance
optional_data: -9999 TO DataPresent instance

"""

print(Contact.objects.count())

d = {
'source_id': 1, 
'product_id': '',
'product_name': 'bom_ghcnd_australia', 
'product_code': '', 
'product_version': '', 
'product_level': ProductLevel.objects.last(), 
'product_uri': 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/stage1/', 
'description': 'temperature precipitation', 
'product_references': ['one', 'two'], 
'product_citation': ['citation 1', 'citation 2'], 
'product_status': ProductStatus.objects.last(), 
'source_format': SourceFormat.objects.last(), 
'source_format_version': '', 
'source_file': '', 
'source_file_checksum': '', 
'data_centre': Organisation.objects.last(), 
'data_centre_url': '', 
'data_policy_licence': DataPolicyLicence.objects.last(),
'contact': [Contact.objects.first().contact_id],
'contact_role': [Role.objects.first().role], 
'history': '', 
'comments': '', 
'timestamp': None, 
'maintenance_and_update_frequency': UpdateFrequency.objects.last(),
'optional_data': DataPresent.objects.last(),
}

try:
    sc =  SourceConfiguration.objects.get(pk=d['source_id'])
    sc.delete()
    print('Deleted previous version\n\n')
except:
    print('No delete happened\n\n')

sc, created = SourceConfiguration.objects.get_or_create(**d)

