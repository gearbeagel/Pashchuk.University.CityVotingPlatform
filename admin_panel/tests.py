from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from voting.models import Project, Comment
from django.utils import timezone


class TestReportProjectView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.staff_user = User.objects.create_user(username='staff_user', password='test_password', is_staff=True)
        self.project = Project.objects.create(name='Test Project', user=self.user, description='Test Description',
                                              pub_date=timezone.now())
        self.client.login(username='staff_user', password='test_password')

    def test_report_project(self):
        response = self.client.get(reverse('report_project', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.project.refresh_from_db()  # Refresh the project instance
        self.assertTrue(self.project.reported_project)  # Ensure the project is reported

        # Ensure the reported_by field is updated with the reporting user
        self.assertIn(self.staff_user, self.project.reported_by.all())

        # Ensure a success message is displayed
        self.assertContains(response, 'Project was reported successfully. Wait for administration to response')

    def tearDown(self):
        self.client.logout()
