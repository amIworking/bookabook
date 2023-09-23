import datetime

from apps.books.models import Book, Author
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')

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
    publish_year = serializers.IntegerField(help_text="books' year publication")

    def __init__(self, *args, **kwargs):
        self.publish_year = None
        super().__init__(*args, **kwargs)

    def validate_year(self, value):
        self.publish_year = value
        if not (0 < value < datetime.date.today().year+1):
            error_message = ("can not be bigger"
            "than current year and can not be less"
             "than 0")
            raise serializers.ValidationError(error_message)
        return self.publish_year


class ShowBooksByYears(serializers.Serializer):
    year1 = serializers.IntegerField(
        help_text="start books' year publication")
    year2 = serializers.IntegerField(
        help_text="end books' year publication")

    def __init__(self, *args, **kwargs):
        self.year1, self.year2 = None, None
        super().__init__(*args, **kwargs)

    def validate_years(self, value):
        try:
            years = value.split('-')
            self.year1, self.year2 = int(years[0]), int(years[1])
        except Exception as e:
            error_message = f"Something went wrong: {str(e)}"
            raise serializers.ValidationError(error_message)



        return value