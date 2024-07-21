from worker.models import City


class CityRepository:
    model: City = City

    @classmethod
    def get(cls, city_name: str):
        return cls.model.objects.get(name=city_name)

    @classmethod
    def create(cls, city_name: str):
        return cls.model.objects.create(name=city_name)

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

