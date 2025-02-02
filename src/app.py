from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os, sys
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# export path
dir_path = os.path.dirname(os.path.realpath(__file__))
print('dirpath', dir_path)
sys.path.append(dir_path)
from src.controllers.variant import *
from src.db.db import mongo
from src.controllers.auth import RegisterApi, AuthApi, RefreshApi

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"] # applies to all routes by default
)

def create_app(config_filename):
    allowed_origins = os.getenv('allowedOrigins').split(' ')
    CORS(app, origins=allowed_origins, allow_headers=["Content-Type", "Authorization"], supports_credentials=True)

    app.config.from_object(config_filename)
    mongo.init_app(app)
    api = Api(app)

    api.add_resource(RegisterApi, '/flask-demo/api/register')
    api.add_resource(RefreshApi, '/flask-demo/api/refresh')
    api.add_resource(AuthApi, '/flask-demo/api/user_auth/<id>')
    api.add_resource(VariantsApi, '/flask-demo/api/variants')
    api.add_resource(VariantApi, '/flask-demo/api/variants/<id>')
    return app



if __name__ == '__main__':
    my_app = create_app('config.BaseConfig')
    my_app.run(host='0.0.0.0', port=5002, debug=os.getenv('isDev'), use_reloader=True)
