from flask import Flask
from flask_restful import Api
from db import db
from resources.variant import Variant


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.mongo.init_app(app)
    api = Api(app)

    api.add_resource(Variant, '/flask-demo/api/variant')
    return app


if __name__ == '__main__':
    my_app = create_app('config.BaseConfig')
    my_app.run(debug=True)
