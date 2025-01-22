from flask_restful import Resource
from flask import request, make_response, jsonify
from pymongo.collection import Collection
from pydantic import ValidationError
from services.variant_service import *
from db import db


class VariantsApi(Resource):
    def __init__(self):
        """Init db cursor"""
        self.variant_cltn: Collection = db.mongo.db['variants']

    # get all 
    def get(self):
        """Get all variants"""
        try:
            return get_variants(self.variant_cltn, 'variants')
        except ValidationError as err:
            print('error', err)
            response = format_error_message(INVALID_VARIANT_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)

    # create new variant
    def post(self):
        """Save a new variant to db"""
        try:
            body = request.get_json()
            print(body)
            return save_variant(self.variant_cltn, 'variants', body)
            #return make_response(variant, 200)
        except ValidationError as err:
            response = format_error_message(INVALID_VARIANT_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)


class VariantApi(Resource):
    def __init__(self):
        self.variant_cltn: Collection = db.mongo.db['variants']

    def get(self, id):
        """Get variant from database by id"""
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)
        return find_variant(self.variant_cltn, 'variants', id)

    def put(self, id):
        """Update a variant"""
        body = request.get_json()
        if not id or not body:
            response = format_error_message(BAD_REQUEST,'BAD_REQUEST', 'id')
            return make_response(response.get_json(), response.status_code)

        return update_variant(self.variant_cltn, 'variants', id, body)

    def delete(self, id):
        """Update a variant"""
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)

        return delete_variant(self.variant_cltn, 'variants', id)

