from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('worker.urls', namespace='main')),
    path('api/v1/', include('api.urls', namespace='api'))
]

