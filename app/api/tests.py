from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from body_mass_calculator.models import MainPersonData

TEST_USER_NAME = 'test_user'
TEST_EMAIL = '1@mail.com'
TEST_PASSWORD = 'test_password'


def create_test_user() -> None:
    user = User.objects.create(username=TEST_USER_NAME,
                               email=TEST_EMAIL)
    user.set_password(TEST_PASSWORD)
    user.save()


def create_test_data(username: str) -> None:
    user = User.objects.get(username=username)
    MainPersonData.objects.create(
        person=user,
        name='test_user',
        sex='M',
        age=32,
        height=180,
        weight=99
    )


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        create_test_user()

    def _get_auth_token_response(self,
                                 user: str,
                                 password: str) -> Response:
        url = api_reverse('api:token-auth')
        data = {
            'username': user,
            'password': password
        }
        return self.client.post(url, data, format='json')

    def test_login_user_api(self) -> None:
        response = self._get_auth_token_response(TEST_USER_NAME,
                                                 TEST_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token", 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertGreater(token_len, 0)

    def test_refresh_token_api(self) -> None:
        refresh_url = api_reverse('api:token-refresh')
        response = self._get_auth_token_response(TEST_USER_NAME,
                                                 TEST_PASSWORD)
        token = response.data.get('token', 0)

        refresh_data = {
            'token': token
        }
        refresh_response = self.client.post(refresh_url,
                                            refresh_data,
                                            format='json')
        refreshed_token = refresh_response.data.get('token', 0)
        refreshed_token_len = 0
        if refreshed_token != 0:
            refreshed_token_len = len(refreshed_token)
        self.assertGreater(refreshed_token_len, 0)

    def test_login_user_api_fail(self) -> None:
        response = self._get_auth_token_response('wrong_user',
                                                 'wrong_password')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        token = response.data.get("token", 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertEqual(token_len, 0)


class MainPersonDataAPITestCase(APITestCase):
    def setUp(self) -> None:
        create_test_user()

    def _get_auth_token(self,
                        user: str,
                        password: str) -> str:
        url = api_reverse('api:token-auth')
        data = {
            'username': user,
            'password': password
        }
        response = self.client.post(url, data, format='json')
        return response.data.get('token')

    def _get_add_test_data_response(self) -> Response:
        url = api_reverse('api:main-data')
        data = {
            'name': 'test_user',
            'sex': 'M',
            'age': 32,
            'height': 180,
            'weight': 99
        }
        token = self._get_auth_token(TEST_USER_NAME, TEST_PASSWORD)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        return self.client.post(url, data, format='json')

    def test_add_data(self) -> None:
        response = self._get_add_test_data_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_data(self) -> None:
        create_test_data(TEST_USER_NAME)
        url = api_reverse('api:main-data')
        data = {
            'name': 'test_user',
            'sex': 'F',
            'age': 33,
            'height': 156,
            'weight': 55
        }
        token = self._get_auth_token(TEST_USER_NAME, TEST_PASSWORD)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
