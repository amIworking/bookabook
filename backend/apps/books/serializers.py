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
    rating_review = serializers.IntegerField(max_value=5, min_value=1)
    class Meta:
        model = BookReview
        #fields = ('__all__')
        fields= ('pk', 'text_review', 'user', 'book', 'rating_review')

class BookReviewChangeSerializer(BookReviewSerializerBase):
    pass


class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= ('pk', 'title', 'slug', 'author', 'rating')





