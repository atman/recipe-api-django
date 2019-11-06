from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # Setup needs to be named exactly as this
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@druk.com',
            password='admin42'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@druk.com',
            password='test123',
            name='Test user'
        )

    def test_users_listed(self):
        """Test that checks if users are listed on the admin page"""
        url = reverse('admin:coreapp_customuser_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:coreapp_customuser_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Tests that the create user page works correctly"""
        url = reverse('admin:coreapp_customuser_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)