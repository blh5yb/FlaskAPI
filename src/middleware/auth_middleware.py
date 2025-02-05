import jwt
from flask import request, abort, make_response
import os
from datetime import datetime, timedelta, timezone

from helpers.helper_functions import logger

from handle_errors import AuthError

jwt_secret = os.getenv('JWT_SECRET')

class AuthMiddleware:

  @staticmethod
  def is_valid_token(token):
    try:
      return jwt.decode(token.split(' ')[1], jwt_secret, algorithms=["HS256"])
    except Exception as e:
      logger.error(e)
      return None

  def authenticate(self):
    access_token  = request.headers.get('Authorization', '')
    refresh_token = request.cookies.get('refreshToken', '')

    print('auth token', access_token, access_token)
    if not access_token and not refresh_token:
      raise AuthError('No auth token provided')
      #print('no auth token')
      #abort(401, 'No auth token provided')

    valid_auth = self.is_valid_token(access_token)
    if not valid_auth:
      if not refresh_token:
        raise AuthError('No auth token provided')
        # raise SystemError('No auth token provided')

      valid_auth = self.is_valid_token(refresh_token)
      if not valid_auth:
        #raise SystemError('No auth token provided')
        raise AuthError('No auth token provided')

      refreshed_user = jwt.encode(
        {'user_id': valid_auth['_id'], 'exp': datetime.now(timezone.utc) + timedelta(hours=24)},
        jwt_secret, algorithm="HS256"
      )
      return refreshed_user

    return

def require_authentication(func):
  def wrapper(*args, **kwargs):
    refreshed_user = AuthMiddleware().authenticate()
    response = func(*args, **kwargs)
    if refreshed_user:  # add refresh info to response
      response.headers['Authorization'] = refreshed_user['idToken']
      response.set_cookie('refreshToken', refreshed_user['refreshToken'], max_age=60 * 60 * 24, httponly=True,
                          samesite='strict')

    return make_response(response.get_json(), response.status_code)

  return wrapper