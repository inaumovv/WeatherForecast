from worker.models import SearchQuery


class SearchHistoryRepository:
    model: SearchQuery = SearchQuery

    @classmethod
    def create(cls, session_key: str, city_id: int):
        return cls.model.objects.create(session_key=session_key, city_id=city_id)

    @classmethod
    def get_with_relations(cls, session_key: str, fields: tuple | list = None):
        return cls.model.objects.filter(session_key=session_key).select_related('city').values(
            *fields if fields else '__all__'
        )
