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
        self.assertTemplateUsed(response, 'homepage/homepage.html')

    def test_profile_view_authenticated(self):
        # Create a test user and log in
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        # Make a GET request to the profile view
        response = self.client.get(reverse('profile'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'homepage/profile.html')

    def test_profile_view_not_authenticated(self):
        # Make a GET request to the profile view without logging in
        response = self.client.get(reverse('profile'))
        # Check if the response status code is 302 (redirect to homepage)
        self.assertEqual(response.status_code, 302)
        # Check if the username context variable is None
        self.assertIsNone(response.context and response.context.get('username'))


class UpdateUsernameTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_update_username(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('update_username'), {'new_username': 'new_test_username'})
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirect
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_test_username')

    def test_update_username_empty(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('update_username'), {'new_username': ''})
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirect
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, '')  # Username should not be changed


class UpdateProfilePictureTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_update_profile_picture(self):
        self.client.login(username='testuser', password='password123')
        with open('static/images/test_image.png', 'rb') as file:
            response = self.client.post(reverse('update_profile_picture'), {'profile_picture': file})
        self.assertEqual(response.status_code, 302)

    def test_update_profile_picture_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('update_profile_picture'), {})
        self.assertEqual(response.status_code, 302)


