from flask_restful import Resource
from flask import request, make_response, jsonify
from db import db
from models.variant_model import VariantSaveModel
from pymongo.collection import Collection
from pydantic import ValidationError
from err_msg import *


def format_error_message(error_message: error_msg, err_thrown):
    return make_response(jsonify({
        "msg": error_message.msg,
        "err": str(err_thrown),
        "err_code": error_message.err_code
    }),
        error_message.status_code
    )


class Variant(Resource):
    def __init__(self):
        self.variant_cltn: Collection = db.mongo.db['variant']

    def post(self):
        """save variant to mongo database"""
        request_data = request.get_json()
        try:
            variant_save_model = VariantSaveModel(**request_data)
        except ValidationError as err:
            return format_error_message(INVALID_VARIANT_SAVE_ERROR, err)

        try:
            inserted_variant_id = str(self.variant_cltn.insert_one(request_data).inserted_id)
        except Exception as err:
            return format_error_message(DB_INSERTION_ERROR, err)

        return make_response({
            "Inserted variant with _id": inserted_variant_id
        }, 201)

    def get(self):
        """Get variant from database by id"""
        variant_id = request.args.get('id')
        try:
            queried_variant = self.variant_cltn.collection.find_one({"_id": variant_id})
            return queried_variant
        except Exception as err:
            return format_error_message(DB_SEARCH_ERROR, err)
