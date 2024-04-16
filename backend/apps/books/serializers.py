import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Book, Author
from django.utils.text import slugify


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields= ('title', 'rating', 'author', 'slug')

