from flask import Flask
from flask_restful import Api
from controllers.variant import *
from serverless_wsgi import handle_request
import os, sys
from db.db import mongo

# export path
dir_path = os.path.dirname(os.path.realpath(__file__))
print('dirpath', dir_path)
sys.path.append(dir_path)

app = Flask(__name__)

def create_app(config_filename):
    app.config.from_object(config_filename)
    mongo.init_app(app)
    api = Api(app)

    api.add_resource(VariantsApi, '/flask-demo/api/variants')
    api.add_resource(VariantApi, '/flask-demo/api/variants/<id>')
    return app

def handler(event, context):
    #my_app = create_app('config.BaseConfig')
    return handle_request(my_app, event, context)


if __name__ == '__main__':
    my_app = create_app('config.BaseConfig')
    my_app.run(host='0.0.0.0', port=5002, debug=os.getenv('isDev'), use_reloader=True)
