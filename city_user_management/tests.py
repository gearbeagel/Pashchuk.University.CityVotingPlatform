from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        # Make a GET request to the home view
        response = self.client.get(reverse('home'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'city_user_management.html')

    def test_profile_view_authenticated(self):
        # Create a test user and log in
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        # Make a GET request to the profile view
        response = self.client.get(reverse('profile'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'city_user_management/profile.html')
        # Check if the username is passed to the template context
        self.assertEqual(response.context['username'], 'testuser')

    def test_profile_view_not_authenticated(self):
        # Make a GET request to the profile view without logging in
        response = self.client.get(reverse('profile'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'city_user_management/profile.html')
        # Check if the username context variable is None
        self.assertIsNone(response.context['username'])
