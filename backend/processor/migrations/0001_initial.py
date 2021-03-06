# Generated by Django 2.2.4 on 2019-08-06 01:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('review_date', models.DateTimeField()),
                ('url', models.URLField()),
                ('status', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('mission', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('geo_area', models.CharField(max_length=255)),
                ('locations', models.CharField(max_length=255)),
                ('keywords', models.CharField(max_length=255)),
                ('aliases', models.CharField(max_length=255)),
                ('languages', models.CharField(max_length=255)),
                ('ein', models.PositiveIntegerField()),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('fax', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
