from flask_restful import Resource
from flask import request, make_response, jsonify
from pymongo.collection import Collection
from pydantic import ValidationError

import sys, os

from src.app import limiter
from src.middleware.auth_middleware import require_authentication
from src.services.auth_service import create_user, sign_in, refresh_user, delete_user

dir_path = os.path.dirname(os.path.realpath(__file__))
print('dirpath', dir_path)
sys.path.append(dir_path)
from src.helpers.format_error_msg import format_error_message
from src.err_msg import *
from src.db import db


class MongoCursor:
    def __init__(self):
        self.user_cltn: Collection = db.mongo.db['users']

class RegisterApi(MongoCursor, Resource):
    def __init__(self):
        """Init db cursor"""
        super().__init__()  # init mongo cursor

    # @limiter.exempt this decorator would exempt it from default limits
    @limiter.limit("5 per minute")
    def post(self): # register
        try:
            """create a new user"""
            body = request.get_json()
            signed_user = create_user(self.user_cltn, 'users', body)
            res = {"msg": f"Created User!", "data": signed_user}

            response = make_response(res, 201)
            response.headers['Authorization'] = signed_user['idToken']
            response.set_cookie('refreshToken', signed_user['refreshToken'], max_age=60 * 60 * 24, httponly=True, samesite='strict')
            return response

        except ValidationError as err:
            response = format_error_message(INVALID_DATA_ERROR, err, 'users')
            return make_response(response.get_json, response.status_code)


class RefreshApi(Resource):
    @limiter.limit("5 per minute")
    def get(self): # refresh cookie
        refresh_token = request.cookies.get('refreshToken', '')
        return refresh_user(refresh_token)

class AuthApi(MongoCursor, Resource):
    def __init__(self):
        """Init db cursor"""
        super().__init__()

    def post(self): # login
        body = request.get_json()
        return sign_in(self.user_cltn, 'users', body)

    @require_authentication
    def get(self, id): # logout
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, "Missing user id", 'id')
            return make_response((response.get_json(), response.status_code))

        response = make_response("Logged Out", 200)
        response.set_cookie('refreshToken', '', max_age=0, httponly=True, samesite='strict')
        return response

    @require_authentication
    @limiter.limit("5 per minute")
    def delete(self, id): # delete
        if not id:
            response = format_error_message(MISSING_QUERY_PARAMETER, "Missing user id", 'id')
            return make_response((response.get_json(), response.status_code))

        return delete_user(self.user_cltn, 'users', id)
