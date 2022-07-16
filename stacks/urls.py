from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('books/', views.MyBookListView.as_view(), name='book-list'),
    path('books-page-num/', views.book_page_num_agg, name='book-list-pagenum'),
    path('books-genre/', views.book_genre_agg, name='book-list-genre'),
    path('books-date/', views.book_date_agg, name='book-list-date'),
    path('books-search/', views.BookListSearchView.as_view(), name='book-list-search'),
    path('test-up/', views.test_update, name='test'),
    path('', RedirectView.as_view(url='books-geo/'), name='index'),
]
