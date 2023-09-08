import datetime

from django.db import models

# Create your models here.
YEAR_CHOICES = [(r,r) for r in range(1000, datetime.date.today().year+5)]

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории', unique=True)
    description = models.CharField(max_length=1000, verbose_name='Описание', blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']
class Author(models.Model):
     first_name = models.CharField(max_length=100, verbose_name='Имя автора')
     last_name = models.CharField(max_length=100, verbose_name='Фамилия автора')
     birth_year = models.IntegerField(('birth_year'), choices=YEAR_CHOICES, blank=True)
     death_year = models.IntegerField(('death_year'), choices=YEAR_CHOICES, blank=True)
     country = models.CharField(max_length=255, verbose_name='Страна рождения', blank=True)

     class Meta:
         verbose_name = 'Автор'
         verbose_name_plural = 'Авторы'
         ordering = ['last_name']

class Book(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название книги')
    description = models.CharField(max_length=1000, verbose_name='Описание', blank=True)
    authors = models.ManyToManyField(Author,)
    genres = models.ManyToManyField(Genre, blank=True)
    publish_year = models.IntegerField(('year'), choices=YEAR_CHOICES,
                                       default=datetime.datetime.now().year,)
    country = models.CharField(max_length=255, verbose_name='Страна публикации', blank=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['name']
