
import pickle
import pandas


def test_read_chunk():
    fpath = 'chunk-cache/glamod_land_delivery_20180928_source-v6.2/station_configuration/station_configuration_source-v6.2.CHUNK.0000026-0000029.pickle'

    with open(fpath, 'rb') as reader:
       df = pickle.load(reader)

    assert(df.latitude[25] == 52.3)

