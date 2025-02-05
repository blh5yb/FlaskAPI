
from src.services.auth_service import *
from src.err_msg import *
from tests.conftest import *
import pytest
from unittest.mock import patch


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

class TestCreateUser:
    """Auth Service Tests"""
    @patch('jwt.encode')
    def test_sign_jwt(self, jwt_mock):
        jwt_mock.side_effect = [accessToken, refreshToken]
        actual = sign_jwt(parsed_user)

        assert actual == user_auth

    def test_create_user_success(self, mock_user_model, mongo_mock, mock_sign_jwt):
        mock_user_model.return_value.dict.return_value = new_user
        mongo_mock.insert_one.return_value = DbInsertRes(parsed_user['_id'])
        mongo_mock.count_documents.return_value = 0

        mock_sign_jwt.return_value = user_auth
        actual = create_user(mongo_mock, new_user)
        assert actual == user_auth


    def test_create_user_value_error(self, mock_user_model, mongo_mock):
        mongo_mock.count_documents.return_value = 1
        with pytest.raises(Exception) as e:
            result = create_user(mongo_mock, user_auth)
            assert result.status == 500
        # assert f'{e.value}' == 'Email Found'

        mock_user_model.assert_not_called()


class TestSignIn:
    """test signing in"""
    def test_signin_success(self, mock_user_model, mongo_mock, mock_sign_jwt):
        mongo_mock.find_one.return_value = my_login
        mock_user_model.return_value.dict.return_value = my_login
        mock_user_model.return_value.check_password.return_value = True
        mock_sign_jwt.return_value = user_auth

        # user_auth {"msg": f"Found User. Logging In.", "data":  user_auth}
        actual = sign_in(mongo_mock, my_login)
        assert actual == user_auth

    def test_user_not_found(self, mongo_mock, mock_sign_jwt, mock_user_model):
        mongo_mock.find_one.return_value = None
        with pytest.raises(ValueError) as e:
            sign_in(mongo_mock, new_user)

        assert f'{e.value}' == "User Not Found"
        mock_user_model.assert_not_called()
        mock_sign_jwt.assert_not_called()
        #mock_format_error.return_value = ({"msg": "Error"}, 500)
        #expected = ({"msg": "Error"}, 500)
        #actual = sign_in(mongo_mock, new_user)
        #assert actual == expected
        #mock_user_model.check_password.assert_not_called()

    def test_password_mismatch(self, mongo_mock, mock_user_model, mock_sign_jwt):
        mongo_mock.find_one.return_value = my_login
        mock_user_model.return_value.check_password.return_value = False
        with pytest.raises(ValueError) as e:
            sign_in(mongo_mock, new_user)

        assert f'{e.value}' == "Invalid Login Credentials"
        mock_sign_jwt.assert_not_called()

class TestRefresh:
    @patch('jwt.decode')
    @patch('jwt.encode')
    def test_refresh_success(self, mock_encode, mock_decode):
        mock_decode.return_value = {'user_id': 'user_id'}
        mock_encode.return_value = accessToken
        actual = refresh_user(refreshToken)
        assert actual == accessToken
        mock_decode.assert_called_with(refreshToken, os.getenv('JWT_SECRET'), algorithms=["HS256"])

class TestDeleteUser:
    def test_delete_user_success(self, mongo_mock):
        db_test_class = DbInsertRes('id', 1)
        mongo_mock.delete_one.return_value = db_test_class
        result = delete_user(mongo_mock, '679909a6ecd2d7f36f88ef6e')
        assert result.deleted_count == 1
