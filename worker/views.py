from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.shortcuts import render
from django.views.generic import TemplateView, View

from services.repositories.city_repository import CityRepository
from services.repositories.search_history_repository import SearchHistoryRepository
from services.weather.geocoder import Geocoder
from services.mixins.context_data_mixin import ContextDataMixin
from services.weather.openmeteo_client import OpenMeteoClient
from worker.models import City


class IndexView(ContextDataMixin, TemplateView):
    template_name: str = 'index.html'
    title_page: str = 'Главная'


class WeatherForecastView(ContextDataMixin, View):
    geocoder: Geocoder = Geocoder()
    openmeteo_client: OpenMeteoClient = OpenMeteoClient()
    city_repo: CityRepository = CityRepository
    search_history_repo: SearchHistoryRepository = SearchHistoryRepository

    def get(self, request: WSGIRequest, *args, **kwargs):
        city_name: str = request.GET.get('city', 'Москва')
        session_key = self.check_session(request)
        coordinates: dict = self.geocoder.geocoding(city_name)
        if coordinates:
            weather_forecast: dict = self.openmeteo_client.get_weather_forecast(coordinates)
            context = self.get_mixin_context(
                title=f'Прогноз погоды в {city_name}',
                weather_list=weather_forecast.values(),
                city=city_name
            )
            self.update_search_history(city_name, session_key)
            return render(request, 'weather_forecast.html', context)

        return render(request, 'weather_forecast.html')

    def update_search_history(self, city_name: str, session_key: str):
        with transaction.atomic():
            try:
                city: City = self.city_repo.get(city_name=city_name.title())
                city.search_count += 1
                city.save()
            except City.DoesNotExist:
                city: City = self.city_repo.create(city_name=city_name)

            self.search_history_repo.create(session_key, city.id)

    @staticmethod
    def check_session(request: WSGIRequest):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key
