from django.contrib import admin

# Register your models here.
from apps.books.models import (Book, Author, Genre)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','country', 'publish_year', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country', 'publish_year')
    prepopulated_fields = {'slug':['name']}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'country', 'slug')
    list_display_links = ('id','first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'country')
    prepopulated_fields = {'slug': ('first_name','last_name')}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'slug')
    list_display_links = ('id','name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ['name']}

admin.site.register(Book, BookAdmin)

admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre, GenreAdmin)