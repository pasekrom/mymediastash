import json
import urllib.request
import urllib.parse
import urllib.error
import time

import requests
from django.core.exceptions import ObjectDoesNotExist

from django.core.files import File
from django.db import transaction, connections
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, DetailView

from .forms import ImportBooksForm
from .models import Book


def import_books(request):
    if request.method == 'POST':
        form = ImportBooksForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']
            import_books_from_json(json_file)
            return redirect('book-home')
    else:
        form = ImportBooksForm()

    context = {'form': form}
    return render(request, 'book/import.html', context)


def import_books_from_json(file):
    try:
        json_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON file: {e}")
        return

    for book_data in json_data:
        published_date = book_data['date_published']
        published_year = published_date.split('-')[0]  # Extract the year from the date

        # Check if the published_year is a valid integer
        if published_year.isdigit():
            published = int(published_year)
        else:
            published = None

        # Check if the pages is a valid integer
        pages = book_data.get('pages')
        if pages:
            pages = int(pages) if pages.isdigit() else None
        else:
            pages = None

        try:
            existing_books = Book.objects.filter(
                title=book_data['title'],
                author=book_data['author_details'],
                publisher=book_data['publisher'],
                published=published
            )
            if existing_books.exists():
                # Book already exists, skip importing
                continue
        except ObjectDoesNotExist:
            # Book does not exist, proceed with importing
            pass

        # Construct the search query for the book cover image
        search_query = f"{book_data['title']} {book_data['author_details']} {published_year}"

        # Perform an image search and get the URL of the first image result
        image_url = perform_image_search(search_query)

        # Download the image and save it as a File object
        cover_image = download_image(image_url)

        # Handle boolean values appropriately
        signed = book_data['signed'].lower() == 'true'

        book = Book(
            author=book_data['author_details'],
            title=book_data['title'],
            isbn=book_data['isbn'],
            publisher=book_data['publisher'],
            published=published,
            bookshelf=book_data['bookshelf'].strip(','),
            series_details=book_data['series_details'],
            pages=pages,
            notes=book_data['notes'],
            anthology=bool(int(book_data['anthology'])),
            anthology_titles=book_data['anthology_titles'],
            location=book_data['location'],
            signed=signed,
            loaned_to=book_data['loaned_to'],
            description=book_data['description'],
            genre=book_data['genre'],
            language=book_data['language'],
            date_added=timezone.datetime.strptime(book_data['date_added'], '%Y-%m-%d %H:%M:%S'),
            goodreads_book_id=book_data['goodreads_book_id'],
            cover=cover_image
        )
        book.save()


def perform_image_search(query, max_retries=3, timeout=5):
    base_url = "http://covers.openlibrary.org/b/ID/medium.jpg"

    # Check if the query is an ISBN, if so, use it in the URL directly
    if query.isdigit():
        image_url = base_url.replace("ID", f"isbn/{query}")
        return image_url

    # If not an ISBN, perform a text search with the title and author
    search_url = "http://openlibrary.org/search.json"
    params = {
        "q": query,
        "limit": 1
    }

    for retry in range(max_retries + 1):
        try:
            response = requests.get(search_url, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()

            if 'docs' in data and len(data['docs']) > 0:
                # Use the first search result to construct the image URL
                first_result = data['docs'][0]
                cover_id = first_result.get('cover_i')
                if cover_id:
                    image_url = base_url.replace("ID", f"id/{cover_id}")
                    return image_url

            # If no matching results or no cover information, return None
            return None

        except requests.RequestException as e:
            if retry == max_retries:
                print(f"Reached maximum retries. Error: {e}")
            else:
                print(f"An error occurred while performing the image search: {e}. Retrying...")
                time.sleep(1)  # Wait for a short time before retrying

    return None


def download_image(image_url):
    if image_url is None:
        return None

    response = requests.get(image_url)
    if response.status_code == requests.codes.ok:
        # Create a File object from the response content
        image_file = File(response.content)
        return image_file

    return None


def clear_books(request):
    if request.method == 'POST':
        # Clear the Book model and reset UUID fields
        with transaction.atomic():
            # Reset the primary key sequence for the Book model
            connection = connections['default']
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE book_book RESTART IDENTITY CASCADE")

        # Redirect to the book home page or any other desired location
        return redirect('book-home')


class BookHome(TemplateView):
    template_name = 'book/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'