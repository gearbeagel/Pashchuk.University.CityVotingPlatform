from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Vote, UserChoice


class VotingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Test Project', description='Test Description')

    def test_overall_info_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        url = reverse('overall_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/overall_info.html')

    def test_detail_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        url = reverse('detail', args=(self.project.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/detail.html')

    def test_results_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        url = reverse('results', args=(self.project.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/results.html')

    def test_vote_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        vote = Vote.objects.create(project=self.project, choice_text='Choice 1', votes=0)
        url = reverse('vote', args=(self.project.id,))
        response = self.client.post(url, {'vote': vote.id})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful vote

    def test_vote_view_already_voted(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        vote = Vote.objects.create(project=self.project, choice_text='Choice 1', votes=0)
        UserChoice.objects.create(user=user, project=self.project, vote=vote)
        url = reverse('vote', args=(self.project.id,))
        response = self.client.post(url, {'vote': vote.id})
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertContains(response, 'You have already voted for this project.')

    def test_vote_view_no_choice(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        url = reverse('vote', args=(self.project.id,))
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertContains(response, 'You did not select a choice.')
