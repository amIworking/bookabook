from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from apps.users.models import User
#from django.contrib.auth.models import User


class Author(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    birth_date = models.DateTimeField(null=True)
    death_date = models.DateTimeField(null=True)
    country = models.CharField(
            max_length=255, verbose_name='Страна рождения',
            blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True,
        verbose_name='slug')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name']

    def get_absolute_url(self):
        return reverse("book", kwargs={"book_name": self.slug})


class Book(models.Model):

    GENRES = [('fiction','fiction'),
              ('novel','novel'),
              ('narrative','narrative'),
              ('mystery','mystery'),
              ('rom-novel','romance novel'),
              ('sci-fict','science fiction'),
              ('thriller', 'thriller'),
              ('hist-fic', 'historical fiction'),
              ('gen-fic', 'genre fiction'),
              ('horror', 'horror'),
              ('tragedy', 'tragedy')]

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    genre = models.CharField(
            max_length=30, choices=GENRES, default='fiction')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    writing_date = models.DateTimeField(
            null=True,
            verbose_name="date of a publishing date")
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(
            max_length=255, unique=True, db_index=True,
            verbose_name='slug')
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0.0
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['title']




class BookReview(models.Model):

    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text_review = models.TextField(max_length=2000, null=True)
    rating_review = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if (BookReview.objects
                .filter(book=self.book, user=self.user)
                .exists()):
            return Exception(
                "You can't write more than 1 review for a book")

        all_ratings = [r.rating_review
                       for r in BookReview.objects
                       .filter(book=self.book)]
        self.book.rating = round(sum(all_ratings) / len(all_ratings), 1)
        self.book.save()
        super().save(*args, **kwargs)


