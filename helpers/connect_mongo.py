from pymongo.collection import Collection
from db.db import mongo
from flask import make_response
from err_msg import *
from helpers.format_error_msg import format_error_message


def insert_one(my_obj, cltn, cursor):
    try:
        inserted_variant_id = str(cursor.insert_one(my_obj).inserted_id)
        return ({
            "Inserted variant with _id": inserted_variant_id
        }, 201)
    except Exception as err:
        return format_error_message(DB_INSERTION_ERROR, err, cltn)


def find_one(doc_id, cltn, cursor):
    try:
        queried_variant = cursor.find_one({"_id": doc_id})
        return ({
            f"Variant with id {doc_id}": queried_variant
        }, 201)
    except Exception as err:
        return format_error_message(DB_SEARCH_ERROR, err, cltn)
