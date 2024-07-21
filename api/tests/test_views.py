import json

from django.test import TestCase
from rest_framework.response import Response

from worker.models import City


class TestViews(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Test')
        self.city_2 = City.objects.create(name='Test2')

    def test_get_view_valid(self):
        response: Response = self.client.get('/api/v1/city-search-count/')
        data = response.data
        expected_data: list = [
            {
                'name': self.city.name,
                'search_count': self.city.search_count,
            },
            {
                'name': self.city_2.name,
                'search_count': self.city_2.search_count
            }
        ]
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        response: Response = self.client.get('/api/v1/city-search-count/?city=Test')
        data: dict = response.data
        expected_data: dict = {
            'name': self.city.name,
            'search_count': self.city.search_count
        }

        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_get_view_invalid(self):
        response: Response = self.client.get('/api/v1/city-search-count/?city=122324/')
        data: dict = response.data
        expected_data = {'error': 'Object does not exist'}
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)
