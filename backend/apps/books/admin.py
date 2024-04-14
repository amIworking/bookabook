from django.contrib import admin

from .models import Book, Author, BookReview

Book_a = admin.site.register(Book)
Author_a = admin.site.register(Author)
BookReview_ = admin.site.register(BookReview)