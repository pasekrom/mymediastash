# Generated by Django 4.2.2 on 2023-07-12 09:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('isbn', models.CharField(max_length=13)),
                ('publisher', models.CharField(max_length=255)),
                ('date_published', models.DateField()),
                ('bookshelf', models.CharField(max_length=255)),
                ('series_details', models.CharField(max_length=255)),
                ('pages', models.IntegerField()),
                ('notes', models.TextField()),
                ('anthology', models.BooleanField()),
                ('anthology_titles', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('signed', models.BooleanField()),
                ('loaned_to', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('goodreads_book_id', models.CharField(max_length=255)),
                ('cover', models.FileField(upload_to='book_covers/')),
            ],
        ),
    ]
