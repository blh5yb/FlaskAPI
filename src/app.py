from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os, sys

# export path
# from pathlib import Path

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(dir_path)
from controllers.variant import *
from db.db import mongo
app = Flask(__name__)
# bcrypt = Bcrypt(app)

def create_app(config_filename):
    allowed_origins = os.getenv('allowedOrigins').split(' ')
    CORS(app, origins=allowed_origins, allow_headers=["Content-Type", "Authorization"], supports_credentials=True)

    app.config.from_object(config_filename)
    mongo.init_app(app)
    api = Api(app)

    # handle errors
    from handle_errors import handle_auth_error, AuthError, handle_environment, handle_value_error
    app.register_error_handler(AuthError, handle_auth_error)
    app.register_error_handler(EnvironmentError, handle_environment)
    app.register_error_handler(ValueError, handle_value_error)

    from controllers.auth import RegisterApi, AuthApi, RefreshApi
    api.add_resource(RegisterApi, '/flask-demo/api/register')
    api.add_resource(RefreshApi, '/flask-demo/api/refresh')
    api.add_resource(AuthApi, '/flask-demo/api/user_auth', '/flask-demo/api/user_auth/<id>')
    api.add_resource(VariantsApi, '/flask-demo/api/variants')
    api.add_resource(VariantApi, '/flask-demo/api/variants/<id>')
    return app



if __name__ == '__main__':
    my_app = create_app('config.BaseConfig')
    my_app.run(host='0.0.0.0', port=5003, debug=os.getenv('isDev'), use_reloader=True)
