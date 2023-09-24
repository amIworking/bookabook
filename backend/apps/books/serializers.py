import datetime

from apps.books.models import Book, Author
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class ShowBook(serializers.Serializer):
    slug = serializers.CharField(help_text="book's slug")
    def __init__(self, *args, **kwargs):
        self.slug = None
        super().__init__(*args, **kwargs)

    def validate_slug(self, value):
        self.slug = value
        book = (Book.objects
                      .filter(slug=self.slug)
                      .first())
        if not book:
            error_message = "This book doesn't exist"
            raise serializers.ValidationError(error_message)
        return value


class ShowBooksByYear(serializers.Serializer):
    publish_year = serializers.IntegerField(min_value=0,
                    max_value=datetime.date.today().year+1,
                    help_text="books' year publication")

    def save(self, **kwargs):
        publish_year = self.validated_data['publish_year']
        books = (Book.objects
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year=publish_year))
        return books



class ShowBooksByYears(serializers.Serializer):
    year1 = serializers.IntegerField(min_value=0,
            max_value=datetime.date.today().year+1,
            help_text="start books' year publication")
    year2 = serializers.IntegerField(min_value=0,
            max_value=datetime.date.today().year+1,
            help_text="end books' year publication")

    def save(self, **kwargs):
        year1 = self.validated_data['year1']
        year2 = self.validated_data['year2']
        books = (Book.objects
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year__range=(year1, year2)))
        return books
