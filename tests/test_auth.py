
from tests.conftest import *
import json


@pytest.fixture(scope="module")
def mock_create_user():
    with patch('controllers.auth.create_user') as create_user_mock:
        yield create_user_mock

@pytest.fixture(scope="module")
def mock_mongo_constructor(mongo_mock):
    with patch('src.controllers.auth.RegisterApi.__init__') as mongo_cnstr_mock:
        mongo_cnstr_mock.return_value = mongo_mock
        yield mongo_cnstr_mock

class TestUserCreationController:
    #@patch('services.auth_service.create_user')
    # @patch(f'{controllers}/auth.create_user')
    def test_create_user_success(self, mock_create_user, mock_mongo_constructor, client):
        my_user = {
            "user": "Barry",
            "idToken": "accessToken",
            "refreshToken": "refreshToken"
        }
        mock_create_user.return_value = my_user
        response = client.post("/flask-demo/api/register", json={
            "name": "name",
            "email": "email",
            "password": "secretpassword"
        })
        mock_create_user.assert_called()
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['data'] == my_user

    def test_validation_error(self, client, mock_create_user):
        mock_create_user.side_effect = ValueError("Validation Error")
        with pytest.raises(Exception) as e:
            response = client.post("/flask-demo/api/register", json={
                "name": "name",
                "email": "email",
                "password": "secretpassword"
            })
            assert e.value == "Validation Error"
            assert response.status_code == 500


@pytest.fixture(scope="module")
def mock_login_user():
    with patch('controllers.auth.sign_in') as login_user_mock:
        yield login_user_mock

class TestUserLoginController:
    def test_user_login_success(self, mock_login_user, mock_mongo_constructor, client):
        mock_login_user.return_value = user_auth
        response = client.post('/flask-demo/api/user_auth', json=user_auth)

        mock_login_user.assert_called()
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data == {
                "msg": f"Found User. Logging In.",
                "data": user_auth,
        }

    def test_user_login_failure(self, mock_login_user, mock_mongo_constructor, client):
        mock_login_user.side_effect = ValueError("User Not Found")
        with pytest.raises(Exception) as e:
            response = client.post('/flask-demo/api/user_auth', json=user_auth)
            assert e.value == "User Not Found"
            assert response.status_code == 500

    @patch('middleware.auth_middleware.AuthMiddleware.authenticate')
    def test_logout_success(self, mock_authenticate, client):
        my_user = {
            "user": "Barry",
            "idToken": "accessToken",
            "refreshToken": "refreshToken"
        }
        mock_authenticate.return_value = my_user
        headers = {
            "Authorization": "Bearer your_token",
            "Content-Type": "application/json"
        }
        response = client.get('/flask-demo/api/user_auth/user_id', headers=headers)
        assert response.status_code == 200

    # @patch('middleware.auth_middleware.AuthMiddleware.authenticate')
    def test_logout_auth_failure(self, client):
        headers = {
            "Authorization": "",
            "Content-Type": "application/json"
        }
        print(client)
        response = client.get('/flask-demo/api/user_auth/user_id', headers=headers)
        assert response.status_code == 401


headers = {
    "Authorization": "Bearer your_token",
    "Content-Type": "application/json"
}
class TestDeleteUserController:
    @patch('middleware.auth_middleware.AuthMiddleware.authenticate')
    @patch('controllers.auth.delete_user')
    def test_delete_user_success(self,  mock_delete_user,mock_authenticate, client):
        mock_delete_user.return_value = DbInsertRes(parsed_user['_id'], 1)
        mock_authenticate.return_value = user_auth
        response = client.delete('/flask-demo/api/user_auth/user_id', headers=headers)
        result = json.loads(response.data)
        mock_delete_user.asser_called()
        mock_authenticate.assert_called()
        assert response.status_code == 200
        assert result == {
                "msg": f"Deleted User",
                "data": {"delete count": 1}
            }

    @patch('middleware.auth_middleware.AuthMiddleware.authenticate')
    @patch('controllers.auth.delete_user')
    def test_delete_user_failure(self,  mock_delete_user,mock_authenticate, client):
        mock_delete_user.side_effect = Exception("Deletion error")
        with pytest.raises(Exception) as e:
            client.delete('/flask-demo/api/user_auth/user_id', headers=headers)
            assert e.value == "Deletion error"

class TestRefreshController:
    @patch('controllers.auth.refresh_user')
    def test_refresh_user_success(self, mock_refresh_user, client):
        mock_refresh_user.return_value = accessToken
        response = client.get('/flask-demo/api/refresh', json={
            "name": "name",
            "email": "email",
            "password": "secretpassword"
        })
        data = json.loads(response.data)
        mock_refresh_user.assert_called()
        assert response.status_code == 200
        assert data == {"msg": f"Found User. Logging In.", "data": {"accessToken": accessToken}}

    @patch('controllers.auth.refresh_user')
    def test_refresh_user_error(self, mock_refresh_user, client):
        mock_refresh_user.side_effect = Exception("Error refreshing user")
        with pytest.raises(Exception) as e:
            response = client.get('/flask-demo/api/refresh', json={
                "name": "name",
                "email": "email",
                "password": "secretpassword"
            })
            assert e.value == "Error refreshing user"