# Generated by Django 4.2.3 on 2023-10-11 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_alter_author_user_alter_book_user_alter_genre_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='user',
        ),
        migrations.RemoveField(
            model_name='book',
            name='user',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='user',
        ),
    ]
