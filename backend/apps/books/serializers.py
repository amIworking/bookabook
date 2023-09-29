import datetime
from typing import List

from apps.books.models import Book, Author, Genre, validate_year
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class AuthorSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('__all__')


class GenreSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('__all__')
class BookSerializerBase(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=255)
    authors = AuthorSerializerBase(required=False, many=True)
    genres = GenreSerializerBase(required=False, many=True)
    publish_year = serializers.IntegerField(validators=[validate_year],
                   default=str(datetime.datetime.now().year))
    country = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=1000, required=False)

    class Meta:
        model = Book
        fields = ('__all__')


class ShowBookSerializer(serializers.Serializer):
    slug = serializers.CharField(help_text="book's slug")
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))

    def validate_slug(self, value):
        book = self.queryset.filter(slug=value).first()
        if not book:
            error_message = "This book doesn't exist"
            raise serializers.ValidationError(error_message)
        return value

    def save(self):
        slug = self.validated_data['slug']
        book = (self.queryset.get(slug=slug))
        return book


class ShowBooksByYear(serializers.Serializer):
    publish_year = serializers.IntegerField(
        min_value=0, max_value=datetime.date.today().year + 1,
        help_text="books' year publication")

    def save(self, **kwargs):
        publish_year = self.validated_data['publish_year']
        books = (Book.objects.all()
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year=publish_year))
        return books


class ShowBooksByYears(serializers.Serializer):
    year1 = serializers.IntegerField(
        min_value=0, max_value=datetime.date.today().year + 1,
        help_text="start books' year publication")
    year2 = serializers.IntegerField(
        min_value=0, max_value=datetime.date.today().year + 1,
        help_text="end books' year publication")

    def save(self, **kwargs):
        year1 = self.validated_data['year1']
        year2 = self.validated_data['year2']
        books = (Book.objects
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year__range=(year1, year2)))
        return books




class AddBookSerializer(BookSerializerBase):
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))

    def validate_slug(self, value):
        book = (self.queryset
                .filter(slug=value).first())
        if book:
            error_message = "A book with given slug already exits"
            raise serializers.ValidationError(error_message)

        return value


    def save(self, **kwargs):
        book = Book.objects.create(**self.validated_data)
        book.save()
        return book


class EditBookSerializer(BookSerializerBase):
    id = serializers.IntegerField()
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))

    def validate_id(self, value):
        book = (self.queryset
                .filter(pk=value)
                .first())
        if not book:
            error_message = "A book with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        self.id = value

        return value


    def validate_slug(self, value):
        pk = self.id
        pre_book = self.queryset.get(pk=pk)
        if pre_book.slug != value:
            book = (self.queryset
                    .filter(slug=value)
                    .first())
            if book:
                error_message = "A book with given slug already exits"
                raise serializers.ValidationError(error_message)
        return value

    def validate(self, attrs):
        return attrs
    def save(self, **kwargs):
        pk = self.validated_data['id']

        self.queryset.filter(pk=pk).update(**self.validated_data)
        return self.queryset.get(pk=pk)

class DeleteBookSerializer(EditBookSerializer):
    queryset = (Book.objects
                .prefetch_related('authors', 'genres'))
    def validate(self, attrs):
        attrs = super().validate(attrs)
        book = self.queryset.get(pk=attrs['id'])
        if book.slug != attrs['slug']:
            error_message = "A slug should be equal to an book instance"
            raise serializers.ValidationError(error_message)
        book.delete()
        return True

class BookToTableBase(serializers.Serializer):
    book_id = serializers.IntegerField()
    author_id = serializers.IntegerField(required=False)
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))
    def validate_book_id(self, value):
        book = (self.queryset
                .filter(pk=value)
                .first())
        if not book:
            error_message = "Book with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        return value


class BookAuthorBase(BookToTableBase):
    author_id = serializers.IntegerField()
    def validate_author_id(self, value):
        author = (Author.objects.all()
                  .filter(pk=value)
                  .first())
        if not author:
            error_message = "Author with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        return value



class AddBookAuthorSerializer(BookAuthorBase):
    def save(self, **kwargs):
        book = self.queryset.get(pk=self.validated_data["book_id"])
        author = Author.objects.get(pk=self.validated_data["author_id"])
        print(book.authors.all())
        if author in book.authors.all():
            error_message = "Author with given id already exists in given book"
            raise serializers.ValidationError(error_message)
        book.authors.add(author)
        return book

class DeleteBookAuthorSerializer(BookAuthorBase):
    def save(self, **kwargs):
        book = self.queryset.get(pk=self.validated_data["book_id"])
        author = Author.objects.get(pk=self.validated_data["author_id"])
        book.authors.remove(author)
        return book

class BookGenreBase(BookToTableBase):
    genre_id = serializers.IntegerField()
    def validate_genre_id(self, value):
        genre = (Genre.objects.all()
                  .filter(pk=value)
                  .first())
        if not genre:
            error_message = "Genre with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        return value



class AddBookGenreSerializer(BookGenreBase):
    def save(self, **kwargs):
        book = self.queryset.get(pk=self.validated_data["book_id"])
        genre = Genre.objects.get(pk=self.validated_data["genre_id"])
        if genre in book.authors.all():
            error_message = "Genre with given id already exists in given book"
            raise serializers.ValidationError(error_message)
        book.genres.add(genre)
        return book

class DeleteBookGenreSerializer(BookGenreBase):
    def save(self, **kwargs):
        book = self.queryset.get(pk=self.validated_data["book_id"])
        genre = Genre.objects.get(pk=self.validated_data["genre_id"])
        book.genres.remove(genre)
        return book

class ShowAuthorSerializer(serializers.Serializer):
    slug = serializers.CharField(help_text="authors's slug")

    def validate_slug(self, value):
        author = Author.objects.filter(slug=value).first()
        if not author:
            error_message = "This author doesn't exist"
            raise serializers.ValidationError(error_message)
        return value

    def save(self):
        return Author.objects.get(slug=self.validated_data['slug'])

class AddAuthorSerializer(AuthorSerializerBase):
    def validate_slug(self, value):
        author = Author.objects.filter(slug=value).first()
        if author:
            error_message = "An author with given slug already exits"
            raise serializers.ValidationError(error_message)

        return value


    def save(self, **kwargs):
        author = Author.objects.create(**self.validated_data)
        author.save()
        return author


class EditAuthorSerializer(AuthorSerializerBase):
    id = serializers.IntegerField()
    queryset = Author.objects.all()

    def validate_id(self, value):
        author = (self.queryset.filter(pk=value).first())
        if not author:
            error_message = "An author with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        self.id = value

        return value


    def validate_slug(self, value):
        pk = self.id
        pre_author = self.queryset.get(pk=pk)
        if pre_author.slug != value:
            author = (self.queryset
                    .filter(slug=value)
                    .first())
            if author:
                error_message = "An author with given slug already exits"
                raise serializers.ValidationError(error_message)
        return value

    def validate(self, attrs):
        return attrs
    def save(self, **kwargs):
        pk = self.validated_data['id']
        self.queryset.filter(pk=pk).update(**self.validated_data)
        return self.queryset.get(pk=pk)

class DeleteAuthorSerializer(EditAuthorSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        author = Author.objects.get(pk=attrs['id'])
        if author.slug != attrs['slug']:
            error_message = "An author should be equal to an author's instance"
            raise serializers.ValidationError(error_message)
        author.delete()
        return True


class ShowGenreSerializer(serializers.Serializer):
    slug = serializers.CharField(help_text="genre's slug")

    def validate_slug(self, value):
        genre = Genre.objects.filter(slug=value).first()
        if not genre:
            error_message = "This genre doesn't exist"
            raise serializers.ValidationError(error_message)
        return value

    def save(self):
        return Genre.objects.get(slug=self.validated_data['slug'])


class AddGenreSerializer(GenreSerializerBase):
    def validate_slug(self, value):
        genre = Genre.objects.filter(slug=value).first()
        if genre:
            error_message = "A genre with given slug already exits"
            raise serializers.ValidationError(error_message)

        return value

    def save(self, **kwargs):
        genre = Genre.objects.create(**self.validated_data)
        genre.save()
        return genre


class EditGenreSerializer(GenreSerializerBase):
    id = serializers.IntegerField()
    queryset = Genre.objects.all()

    def validate_id(self, value):
        genre = (self.queryset.filter(pk=value).first())
        if not genre:
            error_message = "A genre with given id doesn't exist"
            raise serializers.ValidationError(error_message)
        self.id = value

        return value

    def validate_slug(self, value):
        pk = self.id
        pre_genre = self.queryset.get(pk=pk)
        if pre_genre.slug != value:
            genre = (self.queryset
                      .filter(slug=value)
                      .first())
            if genre:
                error_message = "A genre with given slug already exits"
                raise serializers.ValidationError(error_message)
        return value

    def save(self, **kwargs):
        pk = self.validated_data['id']
        self.queryset.filter(pk=pk).update(**self.validated_data)
        return self.queryset.get(pk=pk)


class DeleteGenreSerializer(EditAuthorSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        genre = Genre.objects.get(pk=attrs['id'])
        if genre.slug != attrs['slug']:
            error_message = "A genre should be equal to an genre instance"
            raise serializers.ValidationError(error_message)
        genre.delete()
        return True