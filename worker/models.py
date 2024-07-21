from django.contrib.sessions.models import Session
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=122, unique=True, verbose_name='Название')
    search_count = models.IntegerField(default=1, verbose_name='Количество запросов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('id',)


class SearchQuery(models.Model):
    session_key = models.CharField(max_length=122, verbose_name='Ключ сессии')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Город')

    def __str__(self):
        return f'{self.session_key} | {self.city.name}'

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ('id',)
