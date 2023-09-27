import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
#YEAR_CHOICES = [(r,r) for r in reversed(range(1000, datetime.date.today().year+1))]
def validate_year(value):
    if value > datetime.date.today().year+1:
        raise ValidationError(_(
            '%(value)s can not be bigger'
            'than current year'))
    elif value < 0:
        raise ValidationError(_(
            '%(value)s has to be greater'
            'or equal than 0 year'))

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории', unique=True)
    description = models.CharField(max_length=1000, verbose_name='Описание', blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']
    def __str__(self):
        return f'{self.name}'

class Author(models.Model):
     first_name = models.CharField(max_length=100, verbose_name='Имя автора')
     last_name = models.CharField(max_length=100, verbose_name='Фамилия автора')
     birth_year = models.PositiveIntegerField(validators=[validate_year], null=True, blank=True)
     death_year = models.PositiveIntegerField(validators=[validate_year], null=True, blank=True)
     country = models.CharField(max_length=255, verbose_name='Страна рождения', null=True, blank=True)
     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')

     class Meta:
         verbose_name = 'Автор'
         verbose_name_plural = 'Авторы'
         ordering = ['last_name',]

     def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Book(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название книги')
    description = models.CharField(max_length=1000, verbose_name='Описание', blank=True)
    authors = models.ManyToManyField(Author,)
    genres = models.ManyToManyField(Genre, blank=True)
    publish_year = models.PositiveIntegerField(validators=[validate_year],
                                       default=str(datetime.datetime.now().year),)
    country = models.CharField(max_length=255, verbose_name='Страна публикации', blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} -- {self.publish_year}'
