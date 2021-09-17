# Generated by Django 3.2.7 on 2021-09-14 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250)),
                ('author', models.TextField(max_length=100)),
                ('genre', models.TextField(max_length=100)),
            ],
        ),
    ]