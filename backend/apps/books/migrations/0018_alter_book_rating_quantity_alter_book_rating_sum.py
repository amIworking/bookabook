# Generated by Django 5.0.4 on 2024-04-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_book_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='rating_sum',
            field=models.BigIntegerField(default=0),
        ),
    ]
