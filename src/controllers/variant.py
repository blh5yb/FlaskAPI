from flask_restful import Resource
from flask import request, make_response, jsonify
from pymongo.collection import Collection
from pydantic import ValidationError

from middleware.auth_middleware import require_authentication
from services.variant_service import *
from db import db
from helpers.format_error_msg import format_error_message
from err_msg import *


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
            response = format_error_message(INVALID_DATA_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)

    # create new variant
    @require_authentication
    def post(self):
        """Save a new variant to db"""
        try:
            body = request.get_json()
            print(body)
            return save_variant(self.variant_cltn, 'variants', body)
            #return make_response(variant, 200)
        except ValidationError as err:
            response = format_error_message(INVALID_DATA_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)


class VariantApi(Resource):
    def __init__(self):
        self.variant_cltn: Collection = db.mongo.db['variants']

    @require_authentication
    def get(self, id):
        """Get variant from database by id"""
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)
        return find_variant(self.variant_cltn, 'variants', id)

    @require_authentication
    def put(self, id):
        """Update a variant"""
        body = request.get_json()
        if not id or not body:
            response = format_error_message(BAD_REQUEST,'BAD_REQUEST', 'id')
            return make_response(response.get_json(), response.status_code)

        return update_variant(self.variant_cltn, 'variants', id, body)

    @require_authentication
    def delete(self, id):
        """Update a variant"""
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)

        return delete_variant(self.variant_cltn, 'variants', id)

