
from flask import make_response, jsonify
from err_msg import *


def format_error_message(error_message: error_msg, err_thrown, cltn):
    my_msg = error_message.msg.replace('%s', cltn)
    my_error = error_message._replace(msg=my_msg)
    return make_response(jsonify({
        "msg": my_error.msg,
        "err": str(err_thrown),
        "err_code": my_error.err_code
    }),
        my_error.status_code
    )
