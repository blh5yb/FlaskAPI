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
            variants = get_variants(self.variant_cltn, 'variants')
            return make_response(jsonify({
                "msg": f'Fetched {len(variants)} variants from db',
                "data": [parse_db_res(variant) for variant in variants]
            }), 200)
        except ValidationError as err:
            response = format_error_message(INVALID_DATA_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)

    # create new variant
    @require_authentication
    def post(self):
        """Save a new variant to db"""
        try:
            body = request.get_json()
            result_id = save_variant(self.variant_cltn, body)
            return make_response(jsonify({
                "msg": f"Inserted variant",
                "data": {"id": f"{result_id}"}
            }), 201)
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
        try:
            if not id:
                response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
                return make_response(response.get_json(), response.status_code)

            result = find_variant(self.variant_cltn, id)
            response = make_response(jsonify({
                "msg": f"Fetched Variant",
                "data": result,
            }), 200)
            return response
        except Exception as err:
            response = format_error_message(DB_SEARCH_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)

    @require_authentication
    def put(self, id):
        """Update a variant"""
        try:
            body = request.get_json()
            if not id or not body:
                response = format_error_message(BAD_REQUEST,'BAD_REQUEST', 'id')
                return make_response(response.get_json(), response.status_code)

            variant_id = update_variant(self.variant_cltn, id, body)
            return make_response(jsonify({
                    "msg": f"Updated Variant",
                    "data": {"_id": variant_id},
            }), 200)
        except (ValidationError, ValueError) as err:
            response = format_error_message(INVALID_DATA_ERROR, err, 'variants')
            return make_response(response.get_json(), response.status_code)

    @require_authentication
    def delete(self, id):
        """Update a variant"""
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, 'MISSING_QUERY_PARAMETER', 'id')
            return make_response(response.get_json(), response.status_code)

        try:
            result = delete_variant(self.variant_cltn, id)
            return make_response(jsonify({
                "msg": f"Deleted {result.deleted_count} Variants",
                "data": {},
            }), 200)
        except Exception as err:
            return format_error_message(DB_UPDATE_ERROR, err, 'variants')

