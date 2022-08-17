import pytest
from app import create_app
from db import db
from mongomock import MongoClient
from unittest.mock import patch
import unittest


@pytest.fixture()
def app():
    test_app = create_app('config.BaseConfig')
    test_app.config.update({
        'TESTING': True,
    })

    yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

