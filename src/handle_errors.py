# export path
import os

from flask import make_response

from app import app
from helpers.format_error_msg import format_error_message
from err_msg import UNAUTHORIZED, SERVER_ERROR, UNKNOWN, DB_SEARCH_ERROR
from helpers.helper_functions import logger


class AuthError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message, cltn='users'):
        self.message = message
        self.cltn = cltn

@app.errorhandler(AuthError) # caught the auth middle ware error
def handle_auth_error(e):
      logger.error(f'User unauthorized: {e.message}')
      response = format_error_message(UNAUTHORIZED, e.message, 'auth')
      return make_response(response.get_json(), response.status)


@app.errorhandler(NotFoundError) # caught the auth middle ware error
def handle_db_search_error(e):
      logger.error(f'Data Not Found: {e.message}')
      response = format_error_message(DB_SEARCH_ERROR, e.message, e.cltn)
      return make_response(response.get_json(), response.status)


@app.errorhandler(ValueError)
def handle_value_error(e):
    logger.error(f"Value Error: {e}")
    response = format_error_message(INVALID_DATA_ERROR, e, 'users')
    print(response.get_json())
    return make_response(response.get_json(), response.status)

@app.errorhandler(EnvironmentError)
def handle_environment(err):
    print('env error', err)
    if 'exceeded maximum database items' in err:
        logger.error('exceeded maximum db variants')
        max_variants = os.getenv('MAX_VARIANTS')
        return format_error_message(SERVER_ERROR, err, max_variants)
    else:
        print('unknown error')
        response = format_error_message(UNKNOWN, err,  'unknown')
        return make_response(response.get_json(), response.status)
