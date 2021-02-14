from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


# Helper functions
def sample_user(email='test@gmail.com', password='test123456'):
    return get_user_model().objects.create_user(email, password)


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
            email=email,
            password=password,
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

    def test_tag_str(self):
        """
        Creating TDD for testing tag MODEL
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Abdul'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """
        TDD for testing creation of new ingredient
        """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

