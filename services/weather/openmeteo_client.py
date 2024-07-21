from datetime import datetime

import openmeteo_requests
import pandas as pd
import requests_cache
from babel.dates import format_date
from openmeteo_requests import Client
from openmeteo_sdk.VariablesWithTime import VariablesWithTime
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
from pandas import DatetimeIndex
from requests_cache import CachedSession
from retry_requests import retry

from services.DTOs.weather_dto import WeatherDTO


class OpenMeteoClient:
    url = 'https://api.open-meteo.com/v1/forecast'
    weather_conditionals = {
        0: 'weather_images/clear.png',
        1: 'weather_images/partly_cloudy.png',
        2: 'weather_images/cloudy.png',
        3: 'weather_images/partly_cloudy.png',
        61: 'weather_images/rain.png',
        63: 'weather_images/rain.png',
        65: 'weather_images/rain.png',
        66: 'weather_images/rain.png',
        67: 'weather_images/rain.png',
        71: 'weather_images/snow.png',
        73: 'weather_images/snow.png',
        75: 'weather_images/snow.png',
        77: 'weather_images/snow.png',
        80: 'weather_images/shower.png',
        81: 'weather_images/shower.png',
        85: 'weather_images/snow.png',
        86: 'weather_images/snow.png',
        95: 'weather_images/thunderstorm.png',
    }

    def __get_openmeteo_client(self):
        cache_session: CachedSession = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session: CachedSession = retry(cache_session, retries=5, backoff_factor=0.2)
        return openmeteo_requests.Client(session=retry_session)

    def get_weather_forecast(self, coordinates: dict):
        openmeteo_client: Client = self.__get_openmeteo_client()
        params: dict = {
            'latitude': coordinates['lat'],
            'longitude': coordinates['lng'],
            'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 'wind_speed_10m_max'],
            'timezone': 'Europe/Moscow'
        }
        response: WeatherApiResponse = openmeteo_client.weather_api(self.url, params=params)[0]
        daily_data: WeatherDTO = self.__get_daily_data(response)
        return self.__get_final_data(daily_data)

    @staticmethod
    def __get_daily_data(response: WeatherApiResponse):
        daily: VariablesWithTime = response.Daily()
        daily_date: DatetimeIndex = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )
        daily_data: WeatherDTO = WeatherDTO(
            daily_weather_code=daily.Variables(0).ValuesAsNumpy(),
            daily_temperature_2m_max=daily.Variables(1).ValuesAsNumpy(),
            daily_temperature_2m_min=daily.Variables(2).ValuesAsNumpy(),
            daily_wind_speed_10m_max=daily.Variables(3).ValuesAsNumpy(),
            daily_date=daily_date
        )
        return daily_data

    def __get_final_data(self, daily_data: WeatherDTO):
        final_data: dict = {}
        for i in range(len(daily_data.daily_weather_code)):
            formatted_date: str = self.__format_date(str(daily_data.daily_date[i]))
            weather_image_url: str = self.__get_weather_image_url(int(daily_data.daily_weather_code[i]))
            final_data[i] = {
                'date': formatted_date,
                'image_url': weather_image_url,
                'temperature_max': int(daily_data.daily_temperature_2m_max[i]),
                'temperature_min': int(daily_data.daily_temperature_2m_min[i]),
                'wind_speed_max': int(daily_data.daily_wind_speed_10m_max[i])
            }
        return final_data

    @staticmethod
    def __format_date(date: str):
        date_object: datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return format_date(date_object, format='d MMMM', locale='ru')

    def __get_weather_image_url(self, weather_code: int):
        if weather_code in self.weather_conditionals.keys():
            return self.weather_conditionals[weather_code]
        return self.weather_conditionals[1]


