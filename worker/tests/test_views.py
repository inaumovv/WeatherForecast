from django.db.models import QuerySet
from django.test import TestCase
from rest_framework.response import Response

from worker.models import SearchQuery


class TestViews(TestCase):
    def setUp(self):
        self.client.session.create()

    def test_view_valid(self):
        response: Response = self.client.get('/weather-forecast/?city=Москва')
        search_query: QuerySet[SearchQuery] = SearchQuery.objects.filter(city__name='Москва')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(search_query.exists())

    def test_view_invalid(self):
        response: Response = self.client.get('/weather-forecast/?city=234324')
        search_query: QuerySet[SearchQuery] = SearchQuery.objects.filter(city__name='234324')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(search_query.exists())