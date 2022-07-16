from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('books/', views.view_all_books, name='book-list'),
    path('books-page-num/', views.book_page_num_agg, name='book-list-pagenum'),
    path('books-genre/', views.book_genre_agg, name='book-list-genre'),
    path('books-date/', views.book_date_agg, name='book-list-date'),
    path('books-search/', views.book_search_view, name='book-list-search'),
    path('books-search/book-add/', views.add_book, name='book-add'),
    path('', RedirectView.as_view(url='books/'), name='index'),
]
