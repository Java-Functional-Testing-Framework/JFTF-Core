from logging import getLogger
from json import dumps
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.test_logger = getLogger(f"Test logger {AuthenticationTestCase.__name__}")
        self.signup_url = '/api/auth/signup/'
        self.login_url = '/api/rest-auth/login/'
        self.logout_url = '/api/rest-auth/logout/'
        self.user_url = '/api/rest-auth/user/'
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

    def Test_signup(self):
        self.test_logger.info(f"{self.signup_url} registering user with data {self.user_data}")
        response = self.client.post(self.signup_url, data=self.user_data, format='json')
        self.test_logger.info(f"{self.signup_url} API endpoint status '{response.status_code}'")
        user_existence_status = get_user_model().objects.filter(username=self.user_data['username']).exists()
        self.test_logger.info(f"User existence status '{user_existence_status}'")
        self.assertTrue(user_existence_status)

    def Test_login(self):
        response = self.client.post(self.login_url, data=dumps(self.login_data), content_type='application/json')
        self.test_logger.info(f"{self.login_url} API response '{response.json()}'")
        self.assertEqual(response.status_code, 200)
        self.assertIn('key', response.json().keys())

    def Test_logout(self):
        response = self.client.post(self.logout_url, data=dumps({}), content_type='application/json')
        self.test_logger.info(f"{self.logout_url} API response '{response.json()}'")
        self.assertEqual(response.status_code, 200)

    def Test_authentication_status(self, invert=False):
        self.test_logger.info(f"Checking authentication status for the session user invert='{invert}'")
        test_user_authentication_status = get_user(self.client).is_authenticated
        self.test_logger.info(f"Authentication status for the session user is '{test_user_authentication_status}'")
        if not invert:
            self.assertTrue(test_user_authentication_status)
        else:
            self.assertFalse(test_user_authentication_status)

    def Test_user_information(self):
        response = self.client.get(self.user_url, content_type='application/json')
        self.test_logger.info(f"{self.user_url} API response '{response.json()}'")
        self.assertIn(self.user_data['username'], response.json()['username'])
        self.assertIn(self.user_data['email'], response.json()['email'])

    def test_basic_auth(self):
        self.Test_signup()
        self.Test_login()
        self.Test_authentication_status()
        self.Test_user_information()
        self.Test_logout()
        self.Test_authentication_status(invert=True)

    def tearDown(self):
        self.test_logger.info("Deleting user data from test database")
        get_user_model().objects.filter(username=self.user_data['username']).delete()
