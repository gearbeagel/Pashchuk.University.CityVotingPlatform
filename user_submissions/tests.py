from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserSubmission


class ProposalSubmissionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        self.submission = UserSubmission.objects.create(name='Test Proposal', description='Test Description')

    def test_submit_proposal_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('submit_proposal'))
        self.assertEqual(response.status_code, 200)

    def test_submit_proposal_view_post_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('submit_proposal'), {'name': 'Test Proposal', 'description': 'Test '
                                                                                                         'Description'})
        self.assertEqual(response.status_code, 302)

    def test_submit_proposal_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('submit_proposal'))
        self.assertEqual(response.status_code, 302)

    def test_approve_proposal_view_authenticated_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('approve_proposal', args=[self.submission.pk]))
        self.assertEqual(response.status_code, 302)

    def test_approve_proposal_view_post_authenticated_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('approve_proposal', args=[self.submission.pk]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)

    def test_approve_proposal_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('approve_proposal', args=[self.submission.pk]))
        self.assertEqual(response.status_code, 302)

    def test_approve_proposal_view_redirect_non_staff(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('approve_proposal', args=[self.submission.pk]))
        self.assertEqual(response.status_code, 302)

    def test_proposals_view_authenticated_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('proposals'))
        self.assertEqual(response.status_code, 200)

    def test_proposals_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('proposals'))
        self.assertEqual(response.status_code, 302)
