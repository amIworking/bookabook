import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Book, Author
from django.utils.text import slugify

class BookModel:

    def __init__(self, title: str, genre: str, author_id: int):
        self.title = title
        self.genre = genre
        self.author_id = author_id

class BookSerializer(serializers.Serializer):


    GENRES = [('fiction', 'fiction'),
              ('novel', 'novel'),
              ('narrative', 'narrative'),
              ('mystery', 'mystery'),
              ('rom-novel', 'romance novel'),
              ('sci-fict', 'science fiction'),
              ('thriller', 'thriller'),
              ('hist-fic', 'historical fiction'),
              ('gen-fic', 'genre fiction'),
              ('horror', 'horror'),
              ('tragedy', 'tragedy')]

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000, required=False)
    genre = serializers.ChoiceField(choices=GENRES)
    author_id = serializers.IntegerField(required=False)
    #time_create = serializers.DateTimeField(required=False)
    #time_update = serializers.DateTimeField(required=False)
    writing_date = serializers.DateTimeField(required=False)
    is_published = serializers.BooleanField(default=True)
    slug = serializers.SlugField()


    def slug_existing(self):
        if Book.objects.filter(slug=self.slug).exists():
            return None


    def create(self, validated_data):
        try:
            book = Book.objects.create(**validated_data)
            return book
        except Exception as e:
            return str(e)


    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.writing_date = validated_data.get('writing_date', instance.writing_date)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


def encode():
    model = BookModel(title='test', genre='horror', author_id=1)
    model_sr = BookSerializer(model)
    print(model_sr.data)
    json = JSONRenderer().render(model_sr.data)
    print(json)

def decode():
    stream = io.BytesIO(b'{"title":"test", "genre":"horror", "test": 234}')
    data = JSONParser().parse(stream)
    serializer = BookSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)