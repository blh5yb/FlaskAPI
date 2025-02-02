from src.app import app
from serverless_wsgi import handle_request

def handler(event, context):
    #my_app = create_app('config.BaseConfig')
    return handle_request(app, event, context)