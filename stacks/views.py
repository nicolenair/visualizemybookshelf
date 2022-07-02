from django.shortcuts import render
from stacks.models import Book, User
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
from django.views import generic

class MyBookListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list.html' 

    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

class MyBookListGeographyView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list_geography.html' 
    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

class MyBookListDateView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list_date.html' 
    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

class MyBookListGenreView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list_genre.html' 
    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

class BookListSearchView(generic.ListView):
    model = Book
    template_name = 'stacks/book_list_search_result.html' 
    def get_queryset(self):
        return Book.objects.filter(title=self.request.GET.get("searched_title"))

from .models import Book, Genre, Place
from django.db.models import Count, Q, F, Case, When

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def book_geography_agg(request):
    places = Place.objects.annotate(num_books=Count(Case(
        When(book__users=request.user, then=1))))
    print(places)
    return render(request, 'stacks/book_agg_geography.html', {"places": places})

def book_genre_agg(request):
    genres = Genre.objects.annotate(num_books=Count(Case(
        When(book__users=request.user, then=1))))

    return render(request, 'stacks/book_agg_genre.html', {"genres": genres})
