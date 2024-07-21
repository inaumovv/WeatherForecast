from rest_framework import serializers

from worker.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'search_count')
