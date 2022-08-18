from flask_restful import Resource
from flask import request, make_response, jsonify
from db import db
from models.variant_model import VariantSaveModel
from pymongo.collection import Collection
from pydantic import ValidationError
from err_msg import *
from helpers.format_error_msg import format_error_message
from helpers.connect_mongo import *


class Variant(Resource):
    def __init__(self):
        self.variant_cltn: Collection = db.mongo.db['variant']

    def post(self):
        """save variant to mongo database"""
        request_data = request.get_json()
        try:
            variant_save_model = VariantSaveModel(**request_data)
        except ValidationError as err:
            response = format_error_message(INVALID_VARIANT_SAVE_ERROR, err, 'variant')
            return make_response(response.get_json(), response.status_code)

        return insert_one(request_data, 'variant', self.variant_cltn)

    def get(self):
        """Get variant from database by id"""
        if request.args.get('id'):
            variant_id = request.args.get('id')
            return find_one(variant_id, 'variant', self.variant_cltn)
        else:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)
