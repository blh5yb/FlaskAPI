import pytest
from unittest.mock import patch
from helpers import connect_mongo
from pathlib import Path
from tests.conftest import *

resources = Path(__file__).parent / "resources"


class TestMongo:
    """Mongo Connection Tests"""
    def test_insert_one(self, mongo_mock):
        """test inserting one record to a collection"""
        my_var = {
            "chr": "chr2",
            "pos": 123,
            "ref": 'A',
            "alt": "T",
            "quality": 80
        }
        return_value = connect_mongo.insert_one(
            my_var, 'variant', mongo_mock
        )
        mongo_mock.insert_one.assert_called_with(my_var)
        assert return_value[1] == 201

        #mongo_mock.insert_one.side_effect = Exception("DB_INSERTION_ERROR")
        #with pytest.raises(Exception):
        #    return_value = connect_mongo.insert_one(
        #        my_var, 'variant', mongo_mock
        #    )
        #    assert return_value[1] == 500

    def test_find_one(self, mongo_mock):
        """test searching one doc"""
        return_value = connect_mongo.find_one(1, 'variant', mongo_mock)
        mongo_mock.find_one.assert_called_with({"_id": 1})
        assert return_value[1] == 201

        #mongo_mock.find_one.side_effect = Exception("DB_SEARCH_ERROR")
        #with pytest.raises(Exception) as e:
        #    return_value = connect_mongo.find_one(
        #        1, 'variant', mongo_mock
        #    )
        #    print(return_value)
