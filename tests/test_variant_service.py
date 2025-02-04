
from src.services.variant_service import *
from src.err_msg import *
from src.tests.conftest import *
from bson.objectid import ObjectId
import pytest

my_var = {
  "_id": ObjectId('679909a6ecd2d7f36f88ef6e'),
  "chr": "chr2",
  "pos": 123,
  "ref": 'A',
  "alt": "T",
  "variant_type": "SUBSTITUTION",
  "quality": 80
}

new_var = {
  "chr": "chr2",
  "pos": 123,
  "ref": 'A',
  "alt": "T",
  "variant_type": "SUBSTITUTION",
  "quality": 80
}

parsed_var = {
  "_id": '679909a6ecd2d7f36f88ef6e',
  "chr": "chr2",
  "pos": 123,
  "ref": 'A',
  "alt": "T",
  "variant_type": "SUBSTITUTION",
  "quality": 80
}


class VariantRes:
  def __init__(self, inserted_id):
    self.inserted_id = inserted_id

  def var(self):
    return str(self.inserted_id)

class TestVariants:
    """Variants Service Tests"""
    def test_get_all(self, mongo_mock):
        expected = {
          'msg': f'Fetched 1 variants from db',
          'data': [parsed_var]
        }
        mongo_mock.find.return_value = tuple([my_var])
        return_value, status = get_variants(mongo_mock, 'variants')
        mongo_mock.find.assert_called()
        assert status == 200
        assert  return_value['msg'] == expected['msg']
        for key, val in expected['data'][0].items():
            assert val == expected['data'][0][key]

    def test_get_all_failure(self, mongo_mock):
        mongo_mock.find.side_effect = Exception("DB_SEARCH_ERROR")
        with pytest.raises(Exception) as e:
            get_variants(mongo_mock, 'variants')
            assert e.value == 'DB_SEARCH_ERROR'

    def test_save_new(self, mongo_mock):
        """test inserting one record to a collection"""
        expected = {
          'msg': f"Inserted variant",
          'data': {"_id": f"{parsed_var['_id']}"}
        }
        my_new_var = VariantRes(parsed_var['_id'])
        mongo_mock.find_one.return_value = None
        mongo_mock.insert_one.return_value = my_new_var
        return_value, status = save_variant(mongo_mock, 'variants', new_var)
        mongo_mock.insert_one.assert_called()
        assert status == 201
        assert  return_value['msg'] == expected['msg']
        assert return_value['data'] == expected['data']

    def test_save_value_error(self, mongo_mock):
        mongo_mock.insert_one.side_effect = ValueError("DB_SAVE_VALUE_ERROR")
        with pytest.raises(Exception) as e:
            save_variant(mongo_mock, 'variants', new_var)
            assert e.value == 'DB_SAVE_VALUE_ERROR'