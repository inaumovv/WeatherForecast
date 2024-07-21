from pydantic import BaseModel

from services.DTOs.DTO import DTO


class WeatherDTO(BaseModel, DTO):
    daily_weather_code: list
    daily_temperature_2m_max: list
    daily_temperature_2m_min: list
    daily_wind_speed_10m_max: list
    daily_date: list
