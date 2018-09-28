rm -fr working_dir
# Complete
python __main__.py test_data/glamod_land_delivery_20180928_test001.zip
# Only Source and Station configs
python __main__.py --stations-only test_data/glamod_land_delivery_20180928_test002.zip
