from django.shortcuts import render
from stacks.models import Book, User
from django.contrib.auth.mixins import PermissionRequiredMixin
from stacks.request_api import MaintainBookDatabase
import plotly.graph_objects as go
import plotly.offline as opy

from .models import Book, Genre, Place
from django.db.models import Count, Q, F, Case, When
# Create your views here.
from django.views import generic

class MyBookListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list.html' 

    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

class MyBookListDateView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'stacks.can_view_personal_bookshelf'
    model = Book
    template_name = 'stacks/book_list_date.html' 
    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)

def book_date_agg(request):
    pagenums = Book.objects.filter(users=request.user)
    trace1 = go.Histogram(x=[p.date_of_pub for p in pagenums])
    figure=go.Figure()
    figure.add_trace(trace1)
    figure.update_layout(
        xaxis_title="Year of Publication",
        yaxis_title="Number of Books",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    figure.update_yaxes(tick0=1, dtick=1)

    div = opy.plot(figure, auto_open=False, output_type='div')
    return render(request, 'stacks/book_agg_hist.html' , {"graph": div})

class BookListSearchView(generic.ListView):
    model = Book
    template_name = 'stacks/book_list_search_result.html' 
    def get_queryset(self):
        return Book.objects.filter(title=self.request.GET.get("searched_title"))

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def book_page_num_agg(request):
    pagenums = Book.objects.filter(users=request.user)
    trace1 = go.Histogram(x=[p.page_num for p in pagenums])
    figure=go.Figure()
    figure.add_trace(trace1)
    figure.update_layout(
        xaxis_title="Page Number",
        yaxis_title="Number of Books",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    figure.update_yaxes(tick0=1, dtick=1)

    div = opy.plot(figure, auto_open=False, output_type='div')
    return render(request, 'stacks/book_agg_pagenums.html', {"graph": div})


def book_genre_agg(request):
    genres = Genre.objects.annotate(num_books=Count(Case(
        When(book__users=request.user, then=1))))
    trace1 = go.Histogram(y=[p.name for p in genres], x=[p.num_books for p in genres], orientation='h')
    figure=go.Figure()
    figure.add_trace(trace1)
    figure.update_layout(
        xaxis_title="Number of Books",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    figure.update_yaxes(tick0=1, dtick=1)

    div = opy.plot(figure, auto_open=False, output_type='div')
    return render(request, 'stacks/book_agg_pagenums.html', {"graph": div})

def test_update(request):
    db_update_obj = MaintainBookDatabase()
    db_update_obj()
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
    }
    return render(request, 'index.html', context=context)