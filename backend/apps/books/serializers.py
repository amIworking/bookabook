import io

from django.db import transaction
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from apps.users.models import User
from apps.books.models import Book, Author, BookReview
from django.utils.text import slugify


class AuthorSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ('time_create', 'time_update')

class AuthorCreateSerializer(AuthorSerializerBase):
    class Meta:
        model = Author
        exclude = ('time_create', 'time_update')


class AuthorChangeSerializer(AuthorSerializerBase):
    class Meta:
        model = Author
        exclude = ('time_create', 'time_update', 'slug')

class BookReviewSerializerBase(serializers.ModelSerializer):
    rating_review = serializers.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = BookReview
        fields = ('id', 'text_review', 'user', 'book', 'rating_review')


class BookReviewCreateSerializer(BookReviewSerializerBase):

    def save(self, **kwargs):
        with transaction.atomic():
            book = (Book.objects.select_for_update()
                                .get(id=self.validated_data['book'].id))
            data = super().save(**kwargs)
            book.rating_sum += self.instance.rating_review
            book.rating_quantity += 1
            book.save()
        return data


class BookReviewChangeSerializer(BookReviewSerializerBase):
    def save(self, **kwargs):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(id=self.instance.book_id)
            old_value = self.instance.rating_review
            data = super().save(**kwargs)
            new_value = self.instance.rating_review
            book.rating_sum -= old_value
            book.rating_sum += new_value
            book.save()
        return data

    class Meta:
        model = BookReview
        fields = ('id', 'text_review', 'user', 'book', 'rating_review')
        read_only_fields = ('id', 'book', 'user')


class BookSerializerBase(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ('id', 'title', 'slug',
                  'author', 'rating', 'genre')

    def get_rating(self, instance):
        if instance.rating_sum > 0 and instance.rating_quantity > 0:
            rating = round(instance.rating_sum / instance.rating_quantity, 1)
        else:
            rating = 0.0
        return rating




class BookRetrieveSerializer(BookSerializerBase):
    author = AuthorSerializerBase()
    reviews = BookReviewSerializerBase(source='bookreview_set', many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'slug',
                  'genre', 'description',
                  'author', 'rating',
                  'reviews')


class BookCreateSerializer(BookSerializerBase):
    class Meta:
        model = Book
        exclude = ('time_create', 'time_update')


class BookChangeSerializer(BookSerializerBase):
    class Meta:
        model = Book
        exclude = ('time_create', 'time_update', 'slug')



