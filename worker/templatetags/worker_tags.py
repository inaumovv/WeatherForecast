from django import template
from django.core.handlers.wsgi import WSGIRequest

from services.repositories.search_history_repository import SearchHistoryRepository

register = template.Library()


@register.simple_tag()
def get_search_history(request: WSGIRequest):
    return SearchHistoryRepository.get_with_relations(
        request.session.session_key, fields=('city__name',)
    ).order_by('city_id').distinct('city_id')[:5]
