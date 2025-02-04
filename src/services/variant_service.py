from datetime import datetime
from models.variant_model import VariantModel
from helpers.format_error_msg import format_error_message
from err_msg import *
from helpers.parse_db_res import parse_db_res
from bson.objectid import ObjectId

def get_variants(cursor, cltn):
    try:
        variants = list(cursor.find())
        return ({
            "msg": f'Fetched {len(variants)} variants from db',
            "data": [parse_db_res(variant) for variant in variants]
        }, 200)
    except Exception as err:
        print('db search err', err)
        return format_error_message(DB_SEARCH_ERROR, err, cltn)


def save_variant(cursor, cltn, variant):
    try:
        variant['created_at'] = datetime.utcnow()
        variant = VariantModel(**variant)
        print(variant)
        found_doc = cursor.find_one(variant.dict(exclude={"created_at", "updated_at"}))
        if found_doc is None:
            result_id = str(cursor.insert_one(variant.dict()).inserted_id)
        else:
            result_id = str(parse_db_res(found_doc)['_id'])
        res = {
            "msg": f"Inserted variant",
            "data": {"_id": f"{result_id}"}
        }
        return res, 201
        # return make_response(f'Inserted variant with _id {variant}', 201)
    except (ValueError, Exception) as err:
        if ValueError:
            return format_error_message(INVALID_DATA_ERROR, err, cltn)
        return format_error_message(DB_INSERTION_ERROR, err, cltn)

def find_variant(cursor, cltn, variant_id):
    try:
        result = cursor.find_one({"_id": variant_id})
        print('res', result.dict())
        if not result:
            return format_error_message(DB_SEARCH_ERROR, "variant not found", cltn)
        return ({
                    "msg": f"Fetched Variant",
                    "data": result.dict(),
                }, 201)
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)

def update_variant(cursor, cltn, variant_id, update):
    try:
        variant = VariantModel(**update)
        cursor.update_one({"_id": ObjectId(variant_id)}, {"$set": variant.dict(exclude={"created_at"})})
        # cursor.update_one({"_id": ObjectId(variant_id)}, {"$set": variant.dict(exclude={"_id", "created_at"})})
        return ({
                    "msg": f"Updated Variant",
                    "data": {"_id": variant_id},
                }, 200)
    except Exception as err:
        print(err)
        return format_error_message(DB_UPDATE_ERROR, err, cltn)

def delete_variant(cursor, cltn, variant_id):
    try:
        result = cursor.delete_one({"_id": ObjectId(variant_id)})
        print(result)
        return ({
            "msg": f"Deleted {result.deleted_count} Variants",
            "data": {},
        }, 200)
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)