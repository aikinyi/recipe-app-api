from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """
    Public TDD for Tags API
    """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Testing login required TDD
        """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """
    Creating TDD for authorizing users with correct login details
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test333@gmail.com',
            'password2'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        TDD for retrieving tags
        """
        Tag.objects.create(
            user=self.user,
            name='Vegan'
        )
        Tag.objects.create(
            user=self.user,
            name='Swalo'
        )
        res = self.client.get(TAGS_URL)

        tag = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tag, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_related_to_user(self):
        """
        Getting tags that are related to users TDD
        """
        user2 = get_user_model().objects.create_user(
            'test3333@gmail.com',
            'password2'
        )

        Tag.objects.create(user=user2, name='Swallo')
        tag = Tag.objects.create(user=self.user, name='Swallo')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)