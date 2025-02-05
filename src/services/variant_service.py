from datetime import datetime
from models.variant_model import VariantModel
from err_msg import *
from helpers.parse_db_res import parse_db_res
from bson.objectid import ObjectId

from handle_errors import NotFoundError


def get_variants(cursor, cltn):
        variants = list(cursor.find())
        return [parse_db_res(variant) for variant in variants]


def save_variant(cursor, variant):
    variant['created_at'] = datetime.utcnow()
    variant = VariantModel(**variant)
    found_doc = cursor.find_one(variant.dict(exclude={"created_at", "updated_at"}))
    if found_doc is None:
        return str(cursor.insert_one(variant.dict()).inserted_id)
    else:
        return str(parse_db_res(found_doc)['_id'])

def find_variant(cursor, variant_id):
        result = cursor.find_one({"_id": ObjectId(variant_id)})
        if not result:
            raise NotFoundError("variant not found", 404, 'variants')
            #return format_error_message(DB_SEARCH_ERROR, "variant not found", cltn)
        return parse_db_res(result)


def update_variant(cursor, variant_id, update):
        variant = VariantModel(**update)
        cursor.update_one({"_id": ObjectId(variant_id)}, {"$set": variant.dict(exclude={"created_at"})})
        # cursor.update_one({"_id": ObjectId(variant_id)}, {"$set": variant.dict(exclude={"_id", "created_at"})})
        return variant_id

def delete_variant(cursor, variant_id):
        result = cursor.delete_one({"_id": ObjectId(variant_id)})
        return result