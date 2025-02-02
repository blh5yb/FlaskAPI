from src.services.auth_service import *
from src.err_msg import *
from src.tests.conftest import *
import pytest
from unittest.mock import patch
from flask import make_response, jsonify



class DbInertRes:
  def __init__(self, inserted_id):
    self.inserted_id = inserted_id

@pytest.fixture(scope="function")
def mock_user_model(app):
    """mock UserModel"""
    with patch('src.services.auth_service.UserModel') as user_model_mock:
        yield user_model_mock

@pytest.fixture(scope="function")
def mock_sign_jwt():
    """mock UserModel"""
    with patch('src.services.auth_service.sign_jwt') as jwt_mock:
        yield jwt_mock

@pytest.fixture(scope="function")
def mock_format_error():
    """mock format error message function"""
    with patch('src.services.auth_service.format_error_message') as error_formatter_mock:
        yield error_formatter_mock

class TestUsers:
    """Auth Service Tests"""
    @patch('jwt.encode')
    def test_sign_jwt(self, jwt_mock):
        jwt_mock.side_effect = [accessToken, refreshToken]
        actual = sign_jwt(parsed_user)

        assert actual == user_auth

    def test_create_user_success(self, mock_user_model, mongo_mock, mock_sign_jwt):
        mock_user_model.return_value.dict.return_value = new_user
        mongo_mock.insert_one.return_value = DbInertRes(parsed_user['_id'])

        mock_sign_jwt.return_value = user_auth
        expected = {"msg": f"Created User!", "data":  user_auth}
        actual, status = create_user(mongo_mock, 'users', new_user)
        assert status == 201
        assert actual == expected


    def test_create_user_value_error(self, mock_user_model, mongo_mock):
        mock_user_model.side_effect = ValueError('Invalid user fields')
        with pytest.raises(Exception) as e:
            create_user(mongo_mock, 'users', user_auth)
            assert e.value == 'Invalid user fields'

    def test_signin_success(self, mock_user_model, mongo_mock, mock_sign_jwt):
        mongo_mock.find_one.return_value = my_login
        mock_user_model.return_value.dict.return_value = my_login
        mock_user_model.return_value.check_password.return_value = True
        mock_sign_jwt.return_value = user_auth

        expected =   {"msg": f"Found User. Logging In.", "data":  user_auth}

        actual, status = sign_in(mongo_mock, 'users', my_login)
        assert status == 200
        assert actual == expected

    def test_user_not_found(self, mongo_mock, mock_format_error, mock_user_model):
        mongo_mock.find_one.return_value = None
        mock_format_error.return_value = ({"msg": "Error"}, 500)
        expected = ({"msg": "Error"}, 500)
        actual = sign_in(mongo_mock, 'users', new_user)
        assert actual == expected
        mock_user_model.check_password.assert_not_called()

    def test_password_mismatch(self, mongo_mock, mock_user_model, mock_format_error, mock_sign_jwt):
        mock_user_model.return_value.check_password.return_value = False
        mock_format_error.return_value = ({"msg": "Password Mismatch"}, 500)
        expected = ({"msg": "Password Mismatch"}, 500)
        actual = sign_in(mongo_mock, 'users', new_user)
        assert actual == expected
        mock_sign_jwt.assert_not_called()

