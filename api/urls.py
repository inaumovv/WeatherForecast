from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('city-search-count/', views.CitySearchCountAPIView.as_view())
]