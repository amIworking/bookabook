import datetime

from apps.books.models import Book, Author, Genre
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')


class ShowBook(serializers.Serializer):
    slug = serializers.CharField(help_text="book's slug")
    queryset = (Book.objects.all()
                      .prefetch_related('authors', 'genres'))
    def validate_slug(self, value):
        book = (self.queryset
                      .filter(slug=value)
                      .first())
        if not book:
            error_message = "This book doesn't exist"
            raise serializers.ValidationError(error_message)
        return value

    def save(self):
        slug = self.validated_data['slug']
        book = (self.queryset.get(slug=slug))
        return book


class ShowBooksByYear(serializers.Serializer):
    publish_year = serializers.IntegerField(min_value=0,
                    max_value=datetime.date.today().year+1,
                    help_text="books' year publication")

    def save(self, **kwargs):
        publish_year = self.validated_data['publish_year']
        books = (Book.objects.all()
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

class ChangeBookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()
    def validate_authors(self, values):
        if values:
            queryset = Author.objects.all()
            self.authors = [queryset.filter(pk=pk).first()
                            for pk in values]
            if any(self.authors) is None:
                error_message = "Given author doesn't exist"
                raise serializers.ValidationError(error_message)
        return values

    def validate_genres(self, values):
        if values:
            queryset = Genre.objects.all()
            self.genres = [queryset.filter(pk=pk).first()
                            for pk in values]
            if any(self.genres) is None:
                error_message = "Given author doesn't exist"
                raise serializers.ValidationError(error_message)
        return values

    def validate_slug(self, value):
        if self.instance:
            book = (Book.objects.all()
                    .prefetch_related('authors', 'genres')
                    .filter(slug = value).first())
            if book:
                error_message = "A book with given slug already exits"
                raise serializers.ValidationError(error_message)

        return value

    def save(self, **kwargs):
        authors = self.validated_data('authors')
        genres = self.validated_data('genres')
        name = self.validated_data('name')
        slug = self.validate_slug('slug')
        if not self.instance:
            book = Book.objects.create(
                name=name, slug=slug,
                authors=authors, genres=genres,
                **kwargs)
            book.save()
