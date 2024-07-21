from django.urls import path

from worker import views

app_name = 'worker'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('weather-forecast/', views.WeatherForecastView.as_view(), name='weather-forecast')
]