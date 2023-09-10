# Generated by Django 4.2.3 on 2023-09-08 20:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(default=0, max_length=255, unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=255, unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
    ]