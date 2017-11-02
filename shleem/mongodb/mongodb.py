"""MongoDB data sources."""

import os
import copy
import json
import urllib.parse
from functools import lru_cache

from pymongo import MongoClient
from strct.general import stable_hash_builtins_strct

from shleem.core import (
    DataSource,
    DataTap,
)
from shleem.shared import SHLEEM_DIR_PATH


MONGODB_SOURCE_TYPE = 'MongoDB'
MONGO_CRED_FILE_MSG = (
    'MongoDB credentials for shleem should be set by a credentials file. The '
    'credentials file should be named shleem_mondodb_cred.json, placed in the '
    '.shleem folder located in your home folder and constructed in the '
    'following format:\n'
    '{\n'
    '    "servers": {\n'
    '        "production_data_store": {\n'
    '            "hosts": ["ds192763.mlab.com:51829"],\n'
    '             "username": "shleem_reader",\n'
    '             "password": "8d728673tfi8h723yds"\n'
    '        }\n'
    '    }\n'
    '}'
)


class MongoDBSource(DataSource):
    """A MongoDB data source.

    Arguments
    ---------
    identifier : str
        A string identifier unique to this data source.
    """

    def __init__(self, identifier):
        DataSource.__init__(
            self, identifier=identifier, source_type=MONGODB_SOURCE_TYPE)


SHLEEM_MONGODB_CRED_FNAME = 'shleem_mongodb_cred.json'
SHLEEM_MONGODB_CRED_FPATH = os.path.join(
    SHLEEM_DIR_PATH, SHLEEM_MONGODB_CRED_FNAME)

def _get_cred():
    """Returns MongoDB credentials dict."""
    try:
        with open(SHLEEM_MONGODB_CRED_FPATH, 'r') as mongo_cred_file:
            return json.load(mongo_cred_file)
    except FileNotFoundError: #pragma: no cover
        print(MONGO_CRED_FILE_MSG)


class MongoDBServer(MongoDBSource):
    """A MongoDB server data source.

    Arguments
    ---------
    server_name : str
        The name of this MongoDB server.
    """

    def __init__(self, server_name):
        MongoDBSource.__init__(self, identifier=server_name)
        self.server_name = server_name

    def __repr__(self):
        return "MongoDB server DataSource: {}".format(self.identifier)

    def __getitem__(self, db_name):
        return self.db(db_name)

    def __getattr__(self, db_name):
        return self.db(db_name)

    @lru_cache(maxsize=1024)
    def db(self, db_name):
        """Returns a MongoDBDataBase object with the given name, hosted on this
        MongoDB server."""
        return MongoDBDatabase(self, db_name)

    @staticmethod
    def _mongodb_uris(usr, pwd, hosts):
        parsed_usr = urllib.parse.quote_plus(usr)
        parsed_pwd = urllib.parse.quote_plus(pwd)
        return [
            "mongodb://{usr}:{pwd}@{host}".format(
                usr=parsed_usr, pwd=parsed_pwd, host=host)
            for host in hosts
        ]

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo client connected to this server.

        Returns
        -------
        pymongo.MongoClient
            Returns a pymongo.MongoClient object with reading permissions
            connected to this server.
        """
        cred = copy.deepcopy(_get_cred())
        try:
            server_cred = cred['servers'][self.server_name]
            uris = MongoDBServer._mongodb_uris(
                usr=server_cred.pop('username'),
                pwd=server_cred.pop('password'),
                hosts=server_cred.pop('hosts'),
            )
            print(uris)
            return MongoClient(host=uris, **server_cred)
        except KeyError:
            msg = ("The server {} is missing for shleem's MongoDB credentials"
                   "file.\n".format(self.server_name) + MONGO_CRED_FILE_MSG)
            raise ValueError(msg)


@lru_cache(maxsize=1024)
def server(server_name):
    """Returns a MongoDBServer object with the given name."""
    return MongoDBServer(server_name)


class MongoDBDatabase(MongoDBSource):
    """A specific MongoDB database data source.

    Arguments
    ---------
    mongodb_server : MongoDBServer
        The MongoDB server this database is located on.
    db_name : str
        The name of the database.
    identifier : str, optional
        A string identifier unique to this data source. If none is given, a
        concatenation of the database name to the server identifier is used.
    """

    def __init__(self, mongodb_server, db_name, identifier=None):
        if identifier is None:
            identifier = mongodb_server.identifier + '.' + db_name
        MongoDBSource.__init__(self, identifier=identifier)
        self.mongodb_server = mongodb_server
        self.db_name = db_name

    def __repr__(self):
        return "MongoDB database DataSource: {}".format(self.identifier)

    @lru_cache(maxsize=1024)
    def __getitem__(self, collection_name):
        return MongoDBCollection(self, collection_name)

    def __getattr__(self, collection_name):
        return self[collection_name]

    def collection(self, collection_name):
        """Returns a MongoDBCollection data source object with the given name,
        located at this MongoDB database."""
        return self[collection_name]

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo.database.Database object connected to this
        database."""
        return self.mongodb_server._get_connection()[self.db_name]


class MongoDBCollection(MongoDBSource):
    """A specific MongoDB collection data source.

    Arguments
    ---------
    mongodb_db : MongoDBDatabase
        The MongoDB database this collection is located on.
    collection_name : str
        The name of the collection.
    identifier : str, optional
        A string identifier unique to this data source. If none is given, a
        concatenation of the collection name to the database identifier is
        used.
    """

    def __init__(self, mongodb_db, collection_name, identifier=None):
        if identifier is None:
            identifier = mongodb_db.identifier + '.' + collection_name
        MongoDBSource.__init__(self, identifier=identifier)
        self.mongodb_db = mongodb_db
        self.collection_name = collection_name

    def __repr__(self):
        return "MongoDB collection DataSource: {}".format(self.identifier)

    def query(self, query_dict):
        """Returns a MongoDBQuery source object representing a query ran
        against this collection.

        Arguments
        ---------
        query_dict : dict
            A pymongo-compliant MongoDB query.
        """
        return MongoDBQuery(self, query_dict)

    def aggregation(self, aggregation_pipeline):
        """Returns a MongoDBAggregation source object representing an
        aggregation ran against this collection.

        Arguments
        ---------
        aggregation_piepline : list
            A pymongo-compliant MongoDB aggregation given as a list of dicts.
        """
        return MongoDBAggregation(self, aggregation_pipeline)

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo.collection.Collection object connected to this
        database."""
        return self.mongodb_db._get_connection()[self.collection_name]


class MongoDBQuery(MongoDBSource, DataTap):
    """A specific MongoDB query data source.

    Arguments
    ---------
    mongodb_collection : MongoDBCollection
        The MongoDB collection this query will be ran against.
    query : dict
        A pymongo-compliant MongoDB query.
    identifier : str, optional
        A string identifier unique to this data source. If none is given, a
        concatenation of the collection name to the database identifier is
        used.
    """

    def __init__(self, mongodb_collection, query, identifier=None):
        if identifier is None:
            identifier = mongodb_collection.identifier + '.' + str(
                stable_hash_builtins_strct(query))
        super().__init__(identifier=identifier)
        self.mongodb_collection = mongodb_collection
        self.query = query

    def __repr__(self):
        return "MongoDB query DataSource: {}".format(self.identifier)

    def tap(self):
        col_obj = self.mongodb_collection._get_connection()
        return col_obj.find(self.query)


class MongoDBAggregation(MongoDBSource, DataTap):
    """A specific MongoDB aggregation data source.

    Arguments
    ---------
    mongodb_collection : MongoDBCollection
        The MongoDB collection this query will be ran against.
    aggregation_pipeline : list
        A pymongo-compliant MongoDB aggregation pipelien, given as a list of
        dicts.
    identifier : str, optional
        A string identifier unique to this data source. If none is given, a
        concatenation of the collection name to the database identifier is
        used.
    """

    def __init__(self, mongodb_collection, aggregation_pipeline,
                 identifier=None):
        if identifier is None:
            agg_hash = str(stable_hash_builtins_strct(aggregation_pipeline))
            identifier = mongodb_collection.identifier + '.' + agg_hash
        super().__init__(identifier=identifier)
        self.mongodb_collection = mongodb_collection
        self.aggregation_pipeline = aggregation_pipeline

    def __repr__(self):
        return "MongoDB aggregation DataSource: {}".format(self.identifier)

    def tap(self):
        col_obj = self.mongodb_collection._get_connection()
        return col_obj.aggregate(self.aggregation_pipeline)
