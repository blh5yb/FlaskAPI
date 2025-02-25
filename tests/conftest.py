import pytest
import sys, os
print('conftest', sys.path)
#current_dir = os.getcwd()
#parent_dir = os.path.dirname(current_dir)
#sys.path.insert(0,parent_dir)

from src.app import create_app
from unittest.mock import patch
from dotenv import load_dotenv

from bson.objectid import ObjectId
@pytest.fixture(scope="session")
def app():
    load_dotenv()

    test_app = create_app('config.BaseConfig')
    test_app.config.update({
        'TESTING': True,
    })

    yield test_app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module")
def mongo_mock(app):
    """create mongo db collection find mock"""
    with patch('db.db.mongo.db') as mock_mongo:
        yield mock_mongo


accessToken = 'access_token'
refreshToken = 'refresh_Token'
hashedPass = "hashedPass123"
my_login = {
    "_id": ObjectId('679909a6ecd2d7f36f88ef6e'),
    "name": "Barry",
    "email": "test@email.com",
    "password": hashedPass
}

new_user = {
    "name": "Barry",
    "email": "test@email.com",
    "password": "secretPassword"
}

parsed_user = {
    "_id": "abc",
    "name": "Barry",
    "email": "test@email.com",
    "password": "secretPassword"
}
user_auth = {
    'name': parsed_user['name'],
    'email': parsed_user['email'],
    'localId': str(parsed_user['_id']),
    'registered': True,
    'expiresIn': 60 * 60 * 24,
    'idToken': accessToken,
    'refreshToken': refreshToken
}

@pytest.fixture(scope="function")
def bcrypt_mock(app):
    """mock bcrypt"""
    with patch('bcrypt') as mock_bcrypt:
        mock_bcrypt.hashpw.return_value = hashedPass
        yield mock_bcrypt

#@pytest.fixture(scope="function")
#def mock_create_user():
#    with patch('src.controllers.services.auth.create_user') as create_user_mock:
#        yield create_user_mock


class DbInsertRes:
    def __init__(self, inserted_id, deleted_count = 1):
        self.inserted_id = inserted_id
        self.deleted_count = deleted_count
