from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('books/', views.MyBookListView.as_view(), name='book-list'),
    path('books-geo/', views.book_geography_agg, name='book-list-geo'),
    path('books-genre/', views.book_genre_agg, name='book-list-genre'),
    path('books-date/', views.MyBookListDateView.as_view(), name='book-list-date'),
    path('books-search/', views.BookListSearchView.as_view(), name='book-list-search'),
    path('', RedirectView.as_view(url='books-geo/'), name='index'),
]
