from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """
    Creating Model TDD
    """
    def test_create_user(self):
        """
        Creating test user TDD function
        """
        email = 'aikinyiltd@gmail.com'
        password = '123456'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )
        # Asserting the password and email
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """
        TDD for normalizing email
        """
        email = 'aikinyiltd@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email, 'aikinyiltd',
        )

        # Assertion on email normalization
        self.assertEqual(user.email, email.lower())

    def test_validate_user_email(self):
        """
        Validating user email
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'email address here')
    
    def test_create_superuser(self):
        """
        Creaating superuser
        """
        user = get_user_model().objects.create_superuser(
            'aikinyiltd@gmail.com',
            '123abdcd'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)