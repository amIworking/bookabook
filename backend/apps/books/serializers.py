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
        #fields = ('__all__')
        fields= ('pk', 'first_name', 'last_name')


class BookReviewSerializerBase(serializers.ModelSerializer):
    rating_review = serializers.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = BookReview
        fields= ('pk', 'text_review', 'user', 'book', 'rating_review')


class BookReviewCreateSerializer(BookReviewSerializerBase):

    def save(self, **kwargs):
        with (transaction.atomic()):
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

class BookReviewDestroySerializer(BookReviewSerializerBase):
    pass



class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('pk', 'title', 'slug', 'author')

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        if instance.rating_sum and instance.rating_quantity > 0:
            rating = round(instance.rating_sum / instance.rating_quantity, 1)
        else:
            rating = 0.0
        data['rating'] = rating
        return data


class BookRetrieveSerializer(BookSerializerBase):
    author = AuthorSerializerBase()

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        reviews_queryset = BookReview.objects.filter(book_id=instance.pk)
        reviews = BookReviewSerializerBase(instance=reviews_queryset, many=True)
        data['reviews'] = reviews.data
        return data


class BookCreateSerializer(BookSerializerBase):
    pass


class BookChangeSerializer(BookSerializerBase):
    pass



