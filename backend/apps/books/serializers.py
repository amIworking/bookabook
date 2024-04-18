import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from apps.users.models import User
from .models import Book, Author, BookReview
from django.utils.text import slugify

class UserSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ('pk', 'email', 'first_name', 'last_name')

class AuthorSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Author
        #fields = ('__all__')
        fields= ('pk', 'first_name', 'last_name')
class BookReviewSerializerBase(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    book = serializers.SlugRelatedField(slug_field='title', read_only=True)
    rating_review = serializers.FloatField(read_only=True)
    class Meta:
        model = BookReview
        #fields = ('__all__')
        fields= ('pk', 'text_review', 'user', 'book', 'rating_review')


class BookSerializerBase(serializers.ModelSerializer):
    author = AuthorSerializerBase(read_only=True)
    class Meta:
        model = Book
        fields= ('pk', 'title', 'slug', 'author', 'rating')

class BookChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= ('pk', 'title', 'slug', 'author', 'rating')




