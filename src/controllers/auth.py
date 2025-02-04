from flask_restful import Resource
from flask import request, make_response
from pymongo.collection import Collection
from pydantic import ValidationError

import sys

from src.err_msg import DB_SEARCH_ERROR

print('path', sys.path)
from middleware.limiter_middleware import limiter
from middleware.auth_middleware import require_authentication
from services.auth_service import create_user, sign_in, refresh_user, delete_user
from helpers.format_error_msg import format_error_message
from err_msg import *
from db import db
from helpers.helper_functions import logger


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
            signed_user = create_user(self.user_cltn, body)
            response = make_response({"msg": f"Created User!", "data": signed_user}, 201)
            response.headers['Authorization'] = signed_user['idToken']
            response.set_cookie('refreshToken', signed_user['refreshToken'], max_age=60 * 60 * 24, httponly=True, samesite='strict')
            return response

        except (ValidationError, ValueError) as err:
            print('value error', err)
            logger.error(f"Error registering user: {err}")
            return format_error_message(INVALID_DATA_ERROR, err, 'users')
            #print('err', err, response.status_code)
            #return make_response(response.get_json, response.status_code)


class AuthApi(MongoCursor, Resource):
    def __init__(self):
        """Init db cursor"""
        super().__init__()

    def post(self): # login
        try:
            body = request.get_json()
            user = sign_in(self.user_cltn, body)
            response = make_response({
                "msg": f"Found User. Logging In.",
                "data": user,
            }, 200)
            response.set_cookie('refreshToken', user['refreshToken'], max_age=(60 * 60 * 24))
            return response
        except (ValidationError, ValueError) as err:
            logger.error(f"Error logging in: {err}")
            return format_error_message(DB_SEARCH_ERROR, err, 'users')


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

        try:
            result = delete_user(self.user_cltn, 'users', id)
            response = make_response({
                "msg": f"Deleted User",
                "data": {"delete count": result.deleted_count}
            }, 200)
            response.set_cookie('refreshToken', '', max_age=0)
            return response
        except Exception as err:
            return format_error_message(DB_UPDATE_ERROR, err, 'users')


class RefreshApi(Resource):
    @limiter.limit("5 per minute")
    def get(self): # refresh cookie
        try:
            refresh_token = request.cookies.get('refreshToken', '')
            access_token = refresh_user(refresh_token)
            res = {"msg": f"Found User. Logging In.", "data": {"accessToken": access_token}}
            response = make_response(res, 200)
            response.headers['Authorization'] = access_token
            return response

        except Exception as err:
            logger.error(f"Error refreshing user: {err}")
            return format_error_message(INVALID_DATA_ERROR, err, 'none')