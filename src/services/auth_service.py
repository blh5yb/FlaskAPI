import jwt
import os
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from flask import make_response

from src.err_msg import INVALID_DATA_ERROR, INVALID_TOKEN, DB_SEARCH_ERROR, INVALID_LOGIN, UNKNOWN, DB_UPDATE_ERROR
from src.helpers.format_error_msg import format_error_message
from src.helpers.helper_functions import parse_db_res
from src.models.user_model import UserModel

jwt_secret = os.getenv('JWT_SECRET')

def sign_jwt(user):
    access_token = jwt.encode(
        {'user_id': user['_id'], 'exp': datetime.now(timezone.utc) + timedelta(minutes=60)},
        jwt_secret, algorithm="HS256"
    )
    refresh_token = jwt.encode(
        {'user_id': user['_id'], 'exp': datetime.now(timezone.utc) + timedelta(hours=24)},
        jwt_secret, algorithm="HS256"
    )
    res = {
        'name': user['name'],
        'email': user['email'],
        'localId': str(user['_id']),
        'registered': True,
        'expiresIn': 60 * 60 * 24,
        'idToken': access_token,
        'refreshToken': refresh_token
    }
    return res


def create_user(cursor, cltn, data):
    try:
        user = UserModel(**data)
        result_id = str(cursor.insert_one(user.dict()).inserted_id)
        saved_user = user.dict()
        saved_user['_id'] = result_id
        signed_user = sign_jwt(saved_user)
        return signed_user
    except ValueError as err:
        return format_error_message(INVALID_DATA_ERROR, err, cltn)

def sign_in(cursor, cltn, credentials):
    try:
        result = cursor.find_one({"email": credentials["email"]})
        if not result:
            return format_error_message(DB_SEARCH_ERROR, "user not found", cltn)

        user = UserModel(**result)
        password_match = user.check_password(credentials["password"])
        if not password_match:
            return format_error_message(INVALID_LOGIN, "incorrect password", cltn)
        signed_user = sign_jwt(user.dict())
        response = make_response({
                "msg": f"Found User. Logging In.",
                "data": signed_user,
            }, 200)
        response.set_cookie('refreshToken', signed_user['refreshToken'], max_age=(60 * 60 * 24))
        return response
    except Exception as err:
        return format_error_message(UNKNOWN, err, cltn)


def refresh_user(refresh_token):
    try:
        decoded = jwt.decode(refresh_token, jwt_secret, algorithm="HS256")
        access_token = jwt.encode(
            {'user_id': decoded['_id'], 'exp': datetime.now(timezone.utc) + timedelta(minutes=60)},
            jwt_secret, algorithm="HS256"
        )
        return ({
                "msg": f"Found User. Logging In.",
                "data": {"accessToken": access_token},
        }, 200)
    except Exception as err:
        return format_error_message(INVALID_TOKEN, err, 'none')

def delete_user(cursor, cltn, user_id):
    try:
        result = cursor.delete_one({"_id": ObjectId(user_id)})
        response = make_response({
            "msg": f"Deleted User",
            "data": {"delete count": result.deleted_count}
        }, 200)
        response.set_cookie('refreshToken', '', max_age=0)
        return response
    except Exception as e:
        return format_error_message(DB_UPDATE_ERROR, e, cltn)
