from django.conf.urls import url
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """
    TDD for admin
    """
    def setUp(self):
        """
        Setup function.
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'aikinyiltd@gmail.com',
            password = '1234da'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'aikinyiltda@gmail.com',
            password = '1234da',
            name = 'abdulmutallib'
        )

    def test_users_list(self):
        """
        Testing users list TDD
        """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # Asserting users and password
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Testing User Model
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """
        Adding user TDD
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)