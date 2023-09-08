from apps.books.models import Book, Author
from rest_framework import serializers

class BookSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')