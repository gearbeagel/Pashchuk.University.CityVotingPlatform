from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Vote, Comment, UserChoice


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.project = Project.objects.create(name='Test Project', description='Description of test project')
        self.vote_approve = Vote.objects.create(project=self.project, choice_text='Approve')
        self.vote_disapprove = Vote.objects.create(project=self.project, choice_text='Disapprove')

    def test_detail_view(self):
        url = reverse('detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/detail.html')

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url_nonexistent = reverse('detail', args=[self.project.id + 1])
        response = self.client.get(url_nonexistent)
        self.assertEqual(response.status_code, 404)

    def test_vote_view(self):
        url = reverse('vote', args=[self.project.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.post(url, {'vote': self.vote_approve.id})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url, {'vote': 1000})
        self.assertEqual(response.status_code, 302)

    def test_add_comment_view(self):
        url = reverse('add_comment', args=[self.project.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)

        response = self.client.post(url, {'comment_text': 'Test comment'})
        self.assertEqual(response.status_code, 302)

        UserChoice.objects.create(user=self.user, project=self.project, vote=self.vote_approve)
        response = self.client.post(url, {'comment_text': 'Test comment after voting'})
        self.assertEqual(response.status_code, 302)