from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .views import city_map, get_projects_by_district
from voting.models import Project


class CityMapTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_city_map_view(self):
        url = reverse('city_map')
        request = self.factory.get(url)
        request.user = self.user
        response = city_map(request)
        self.assertEqual(response.status_code, 200)


class GetProjectsByDistrictTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.project1 = Project.objects.create(name='Project 1', description='Description 1', district='District 1')
        self.project2 = Project.objects.create(name='Project 2', description='Description 2', district='District 1')
        self.project3 = Project.objects.create(name='Project 3', description='Description 3', district='District 2')

    def test_get_projects_by_district_view(self):
        url = reverse('get_projects_by_district')
        request = self.factory.get(url, {'district': 'District 1'})
        request.user = self.user
        response = get_projects_by_district(request)
        self.assertEqual(response.status_code, 200)
        data = response.content.decode('utf-8')
        data = eval(data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Project 1')
        self.assertEqual(data[1]['name'], 'Project 2')

    def test_get_projects_by_district_view_invalid_request(self):
        url = reverse('get_projects_by_district')
        request = self.factory.post(url)
        request.user = self.user
        response = get_projects_by_district(request)
        self.assertEqual(response.status_code, 400)
