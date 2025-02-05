import jwt
import os
from datetime import datetime, timedelta, timezone

from bson import ObjectId
# from flask import make_response
# from err_msg import INVALID_DATA_ERROR, INVALID_TOKEN, DB_SEARCH_ERROR, INVALID_LOGIN, UNKNOWN, DB_UPDATE_ERROR
# from helpers.format_error_msg import format_error_message

from models.user_model import UserModel
from helpers.parse_db_res import parse_db_res

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


def create_user(cursor, data):
    cursor.delete_many({'email': data['email']})
    if cursor.count_documents({'email': data['email']}):
        raise ValueError("Email Found")

    user = UserModel(**data)
    result_id = str(cursor.insert_one(user.dict()).inserted_id)
    data['_id'] = result_id
    signed_user = sign_jwt(data)
    return signed_user

def sign_in(cursor, credentials):
    result = cursor.find_one({"email": credentials["email"]})
    if not result:
        raise ValueError("User Not Found")

    parsed_result = parse_db_res(result)
    user = UserModel(**parsed_result)
    password_match = user.check_password(credentials["password"])
    if not password_match:
        raise ValueError("Invalid Login Credentials")

    return sign_jwt(parsed_result)


def refresh_user(refresh_token):
    decoded = jwt.decode(refresh_token, jwt_secret, algorithms=["HS256"])
    return jwt.encode(
        {'user_id': decoded['user_id'], 'exp': datetime.now(timezone.utc) + timedelta(minutes=60)},
        jwt_secret, algorithm="HS256"
    )

def delete_user(cursor, user_id):
    return cursor.delete_one({"_id": ObjectId(user_id)})
