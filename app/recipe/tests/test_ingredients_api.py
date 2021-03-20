from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """
    Public TDD for ingredient
    """
    def setUp(self):
        """
        Setup TDD
        """
        self.client = APIClient()

    def test_login_required(self):
        """
        TDD for testing valid credentials during login
        """
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """
    Private TDD for ingredient
    """
    def setUp(self):
        """
        Setup
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test1@gmail.com',
            'pass1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        Ingredient.objects.create(user=self.user, name='Masa')
        Ingredient.objects.create(user=self.user, name='Towo')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """
        Unit testing for list of ingredient that are limited to users2
        """
        user2 = get_user_model().objects.create_user(
            'test22@gmail.com',
            'pass222'
        )

        Ingredient.objects.create(user=user2, name='Turmeric')
        ingredient = Ingredient.objects.create(user=self.user, name='Garlic')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """
        Unit testing for creating successful ingredient
        """
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """
        Creating test for unsuccessful ingredient creation
        """
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
