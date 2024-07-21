from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CitySerializer
from services.repositories.city_repository import CityRepository
from worker.models import City


class CitySearchCountAPIView(APIView):
    repo: CityRepository = CityRepository
    serializer: CitySerializer = CitySerializer

    def get(self, request):
        city_name = request.GET.get('city', None)
        if request.GET.get('city'):
            try:
                city = self.repo.get(city_name=city_name)
                return Response(self.serializer(city).data)
            except City.DoesNotExist:
                return Response({'error': 'Object does not exist'})

        cities = self.repo.get_all()
        return Response(self.serializer(cities, many=True).data)
