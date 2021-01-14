from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# variable for creating users
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """
    Creating user method
    """
    return get_user_model().objects.create_user(**params)


"""Public API, this allow all users to used it it without authorization """


class PublicUserAPITest(TestCase):
    """
    Test creat user TDD (public api)
    """

    def setUp(self):
        """
        Setting up user
        """
        self.client = APIClient()

    def test_create_valid_user(self):
        """
        Validating user success payload
        """
        payload = {
            'email': 'aikinyiltd@gmail.com',
            'password': 'pass1234',
            'name': 'Abdulmutallib'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """
        Checking if user exist TDD
        """
        payload = {
            'email': 'aikinyiltd@gmail.com',
            'password': 'pass1234',
            'name': 'Abdulmutallib'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        """
        Testing short password TDD
        """
        payload = {
            'email': 'aikinyiltd@gmail.com',
            'password': 'pw',
            'name': 'Abdulmutallib'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    """
    Creating user TOKEN TDD
    """

    def test_create_token_for_user(self):
        """
        Creating token for user TDD
        """
        payload = {'email': 'test@gmail.com', 'password': 'testpassword'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # Making asserting for the TDD
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_token_invalid_credentials(self):
        """
        Creating TDD for testing invalid user credentials
        """
        create_user(email='test@gmail.com', password='password')
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """
        Creating TDD for stopping token creation
        if user does not exist.
        """
        payload = {'email': 'test@gmail.com', 'password': 'testpassword'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_field(self):
        """
        Test that username and password are required
        """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        This TDD test that user most be authenticated before access
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


"""PRIVATE API, this ONLY allow  users to used it it with authorization"""


class PrivateUserApiTest(TestCase):
    """
    TDD for testing authorized users only.
    """
    def setUp(self):
        self.user = create_user(
            email='testing@gmail.com',
            password='password12345',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        TDD for testing successful user profile retrieval
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """
        TDD for blocking post request on the URL
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        TDD for updating users after they are authenticated
        """
        payload = {'name': 'name new', 'password': 'password12341'}

        res = self.client.patch(ME_URL, payload)

        self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
