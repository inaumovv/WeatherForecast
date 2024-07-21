import requests

from weather_forecast import settings


class Geocoder:
    __API_KEY = settings.YANDEX_API_KEY
    __geocoder_url: str = 'https://geocode-maps.yandex.ru/1.x'

    def geocoding(self, city: str):
        response: requests.Response = requests.get(self.__geocoder_url, params={
            'apikey': self.__API_KEY,
            'geocode': city,
            'format': 'json',
        })
        if response.status_code == 200:
            return self.__get_coordinates(response)

        return None

    @staticmethod
    def __get_coordinates(response: requests.Response):
        try:
            data: dict = response.json()
            coordinates: str = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            longitude, latitude = coordinates.split()
            coordinates_dict: dict = {
                'lat': latitude,
                'lng': longitude,
            }
            return coordinates_dict

        except IndexError:
            return None

