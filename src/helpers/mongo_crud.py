from pymongo.collection import Collection
from db.db import mongo
from flask import make_response
from err_msg import *
from helpers.format_error_msg import format_error_message
from bson import json_util
from models.variant_model import VariantModel

from helpers.helper_functions import parse_db_res


# CRUD operations are collection agnostic, so separating logic from services

def insert_one(my_obj, cursor, cltn):
    try:
        #result = cursor.insert_one(my_obj.dict())
        found_doc = cursor.find_one(my_obj)
        if found_doc is None:
            data = VariantModel(**variant)
            return str(cursor.insert_one(data).inserted_id)
        else:
            return str(parse_db_res(found_doc)['_id'])
        #inserted_variant_id = str(cursor.insert_one(my_obj).inserted_id)
        #return ({
        #    "Inserted variant with _id": inserted_variant_id
        #}, 201)
    except Exception as err:
        print('err', err)
        return format_error_message(DB_INSERTION_ERROR, err, cltn)

def find_one(doc_id, cursor, cltn):
    try:
        return cursor.find_one({"_id": doc_id})
        #queried_variant = cursor.find_one({"_id": doc_id})
        #return ({
        #    f"Variant with id {doc_id}": queried_variant
        #}, 201)
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)

def update_one(filter, update, cursor, cltn):
    try:
        return cursor.update_one(filter, {"$set": update.dict()})
    except Exception as err:
        return format_error_message(DB_UPDATE_ERROR, err, cltn)

def delete_one(filter, cursor, cltn):
    try:
        return cursor.delete_one(filter)
    except Exception as err:
        return format_error_message(DB_UPDATE_ERROR, err, cltn)

def fetch_all(cursor, cltn):
    try:
        return list(cursor.find())
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)