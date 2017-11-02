"""Testing MongoDB data sources for the shleem python package."""

import pytest
from strct.general import stable_hash_builtins_strct

import shleem

def test_mongo_sources():

    # defining a MongoDB server source
    shleem_test_server = shleem.mongodb.server("shleem_test_server")
    assert repr(shleem_test_server) == (
        "MongoDB server DataSource: shleem_test_server")
    assert shleem_test_server.identifier == 'shleem_test_server'
    assert shleem_test_server.server_name == 'shleem_test_server'

    # db source
    test_db = shleem_test_server['shleem_test']
    test_db2 = shleem_test_server.shleem_test
    test_db3 = shleem_test_server.db('shleem_test')
    assert test_db == test_db2
    assert test_db2 == test_db3
    assert repr(test_db) == (
        "MongoDB database DataSource: shleem_test_server.shleem_test")
    assert test_db.identifier == 'shleem_test_server.shleem_test'
    assert test_db.db_name == 'shleem_test'

    # collection source
    examp = test_db['example_data_collection']
    examp2 = test_db.example_data_collection
    examp3 = test_db.collection('example_data_collection')
    assert examp == examp2
    assert examp == examp3
    assert repr(examp) == (
        "MongoDB collection DataSource: shleem_test_server.shleem_test"
        ".example_data_collection")
    assert examp.identifier == (
        'shleem_test_server.shleem_test.example_data_collection')
    assert examp.collection_name == 'example_data_collection'

    # query data tap
    query = {"borough": "Queens"}
    queens_people = examp.query(query)
    assert repr(queens_people) == (
        "MongoDB query DataSource: shleem_test_server.shleem_test"
        ".example_data_collection.{}".format(
            stable_hash_builtins_strct(query)))
    assert queens_people.identifier == (
        "shleem_test_server.shleem_test.example_data_collection.{}".format(
            stable_hash_builtins_strct(query)))
    assert queens_people.source_type == 'MongoDB'

    # checking the client
    client = shleem_test_server._get_connection()
    some_doc = client['shleem_test']['example_data_collection'].find_one()
    assert some_doc['restaurant_id'] == '30112340'

    # tapping the source
    cursor = queens_people.tap()
    other_doc = cursor.next()
    assert other_doc['restaurant_id'] == '40356068'

    # aggregation data tap
    agg_pipeline = [
        {'$group': {'_id': '$borough', 'count': {'$sum': 1}}}
    ]
    borough_counts = examp.aggregation(agg_pipeline)
    exp_id = (
        'shleem_test_server.shleem_test.example_data_collection.'
        '7098918b9417525bcb7126c8978ad3c10ac4a352a2238d3e614cfcd50b6b82bc')
    assert borough_counts.identifier == exp_id
    exp_repr = "MongoDB aggregation DataSource: {}".format(exp_id)
    assert repr(borough_counts) == exp_repr

    # tap the source 2: the aggregation strikes back
    cursor = borough_counts.tap()
    res = {doc['_id']: doc['count'] for doc in cursor}
    assert res['Missing'] == 51
    assert res['Queens'] == 5656





def test_missing_server():
    missing_server = shleem.mongodb.server("missing_server")
    with pytest.raises(ValueError):
        client = missing_server._get_connection()
        assert not client.database_names
