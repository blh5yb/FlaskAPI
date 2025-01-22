from models.variant_model import VariantModel
from flask import make_response, jsonify
from helpers.format_error_msg import format_error_message
from err_msg import *
from helpers.mongo_crud import *
from helpers.helper_functions import parse_db_res
from bson.objectid import ObjectId
import json

def get_variants(cursor, cltn):
    try:
        #variants = VariantModel.objects().to_json()
        variants = fetch_all(cursor, cltn)
        return ({
            "msg": f'Fetched {len(variants)} variants from db',
            "data": parse_db_res(variants),
        }, 200)
    except Exception as err:
        print('db search err', err)
        return format_error_message(DB_SEARCH_ERROR, err, cltn)


def save_variant(cursor, cltn, variant):
    try:
        result_id = insert_one(variant, cursor, cltn)

        return ({
            "msg": f'Inserted variant',
            "data": {"_id": result_id},
        }, 201)
        #return make_response(f'Inserted variant with _id {variant}', 201)
    except (ValueError, Exception) as err:
        if ValueError:
            return format_error_message(INVALID_VARIANT_ERROR, err, cltn)
        return format_error_message(DB_INSERTION_ERROR, err, cltn)

def find_variant(cursor, cltn, variant_id):
    try:
        result = find_one(ObjectId(variant_id), cursor, cltn)
        if not result:
            return format_error_message(DB_SEARCH_ERROR, "varaint not found", cltn)
        return ({
            "msg": f'Fetched Variant',
            "data": parse_db_res(result),
        }, 201)
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)

def update_variant(cursor, cltn, variant_id, variant):
    try:
        data = VariantModel(**variant)
        update_one({"_id": ObjectId(variant_id)}, data, cursor, cltn)
        return ({
            "msg": f'Updated Variant',
            "data": {"_id": variant_id},
        }, 200)
    except Exception as err:
        return format_error_message(DB_UPDATE_ERROR, err, cltn)

def delete_variant(cursor, cltn, variant_id):
    try:
        result = delete_one({"_id": ObjectId(variant_id)}, cursor, cltn)
        print(result)
        return ({
            "msg": f'Deleted {result.deleted_count} Variants',
            "data": {},
        }, 200)
    except Exception as err:
        return format_error_message(DB_UPDATE_ERROR, err, cltn)