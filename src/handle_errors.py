# export path
import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
print(dir_path)
print('sys', sys.path)

from src.app import app
from src.helpers.format_error_msg import format_error_message
from src.err_msg import UNAUTHORIZED, SERVER_ERROR, UNKNOWN
from src.helpers.helper_functions import logger

@app.errorhandler(SystemError) # caught the auth middle ware error
def handle_auth_error(e):
      logger.error('User unauthorized', e)
      return format_error_message(UNAUTHORIZED, e, 'auth')

@app.errorhandler(EnvironmentError)
def handle_environment(err):
  if 'exceeded maximum database items' in err:
      logger.error('exceeded maximum db variants')
      max_variants = os.getenv('MAX_VARIANTS')
      return format_error_message(SERVER_ERROR, err, max_variants)
  else:
    return format_error_message(UNKNOWN, err,  'unknown')
