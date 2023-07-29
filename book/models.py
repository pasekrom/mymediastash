import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.datetime_safe import datetime


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.TextField(blank=True)
    title = models.TextField(blank=True)
    isbn = models.TextField(blank=True)
    publisher = models.TextField(blank=True)
    published = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: YYYY",
        null=True,
        blank=True
    )
    bookshelf = models.TextField(blank=True)
    series_details = models.TextField(blank=True)
    pages = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    anthology = models.BooleanField()
    anthology_titles = models.TextField(blank=True)
    location = models.TextField(blank=True)
    signed = models.BooleanField(default=False)
    loaned_to = models.TextField(blank=True)
    description = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    language = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    goodreads_book_id = models.TextField(blank=True)
    cover = models.FileField(upload_to='book_covers/', blank=True, max_length=500)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f'{self.title} - {self.author} / {self.publisher} / {self.published}'
