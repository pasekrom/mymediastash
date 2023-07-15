from django.urls import path

from . import views
from .views import BookHome, import_books, clear_books

urlpatterns = [
    path('', BookHome.as_view(), name='book-home'),
    path('<uuid:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('import-books/', import_books, name='import-books'),
    path('clear-books/', clear_books, name='clear-books'),
]
