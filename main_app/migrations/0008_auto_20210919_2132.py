# Generated by Django 3.2.7 on 2021-09-19 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
