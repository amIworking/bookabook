# Generated by Django 4.2.3 on 2023-09-13 19:54

import apps.books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_author_birth_year_alter_author_death_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birth_year',
            field=models.PositiveIntegerField(blank=True, validators=[apps.books.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_year',
            field=models.PositiveIntegerField(blank=True, validators=[apps.books.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_year',
            field=models.PositiveIntegerField(default='2023', validators=[apps.books.models.validate_year]),
        ),
    ]
