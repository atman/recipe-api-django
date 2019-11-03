from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('userapp:create')
TOKEN_URL = reverse('userapp:token')
PROFILE_URL = reverse('userapp:profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the Users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating a user with valid payload is successful"""
        payload = {
            'email': 'atman@druk.com',
            'password': 'testpass',
            'name': 'test name',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'atman@druk.com',
            'password': 'testpass',
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'atman@druk.com', 'password': 'test123'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not returned in invalid credentials"""
        create_user(email='atman@druk.com', password='qwe123')
        payload = {'email': 'atman@druk.com', 'password': 'test123'}

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that a token is not created if user does not exists"""
        payload = {'email': 'atman@druk.com', 'password': 'test123'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that a token is not created if request does not include all required fields"""
        payload = {'email': 'atman@druk.com', 'password': ''}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Authentication is required for users"""
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@druk.com',
            password='test123',
            name='Test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retriever_user_profile(self):
        """Test retrieving profile for logged in user"""
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that POST is not allowed on this API"""
        response = self.client.post(PROFILE_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Tests that the user data can be updated"""
        payload = {
            'name': 'name',
            'email': 'newpassword'
        }

        response = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password, payload['password'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
