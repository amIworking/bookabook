from django.contrib import admin

# Register your models here.
from apps.books.models import (Book, Author, Genre)

admin.site.register(Book)

admin.site.register(Author)

admin.site.register(Genre)