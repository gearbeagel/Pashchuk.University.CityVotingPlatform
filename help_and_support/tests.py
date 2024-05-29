from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from help_and_support.models import RequestTicket
from help_and_support.forms import RequestTicketForm
from django.core import mail
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class HelpAndSupportViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.help_page_url = reverse('help_page')
        self.submit_ticket_url = reverse('submit_ticket')

        site = Site.objects.get_current()
        self.social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='dummy_client_id',
            secret='dummy_secret',
        )
        self.social_app.sites.add(site)

    def test_help_page_view(self):
        response = self.client.get(self.help_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help_and_support/FAQ.html')

    def test_submit_ticket_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.submit_ticket_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help_and_support/request_ticket.html')
        self.assertIsInstance(response.context['form'], RequestTicketForm)

    def test_submit_ticket_view_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'title': 'Test Ticket',
            'description': 'This is a test ticket description.'
        }
        response = self.client.post(self.submit_ticket_url, data=form_data)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(RequestTicket.objects.count(), 1)

        request_ticket = RequestTicket.objects.first()
        self.assertEqual(request_ticket.title, 'Test Ticket')
        self.assertEqual(request_ticket.description, 'This is a test ticket description.')
        self.assertEqual(request_ticket.user, self.user)

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your request ticket has been saved successfully.')

    def test_submit_ticket_view_post_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'title': '',
            'description': ''
        }
        response = self.client.post(self.submit_ticket_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help_and_support/request_ticket.html')
        self.assertIsInstance(response.context['form'], RequestTicketForm)
        self.assertTrue(response.context['form'].errors)

        self.assertEqual(RequestTicket.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
