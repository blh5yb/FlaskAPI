import os

class BaseConfig:
    DEBUG = os.getenv('isDEV')
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
    #MONGODB_SETTINGS = { Mongo engine way
    #    "host": os.getenv('MONGO_URI')
    #}
