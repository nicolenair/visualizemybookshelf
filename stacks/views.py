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
        books = Book.objects.filter(users=self.request.user)
        return [i.title for i in books]

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    context = {
        'num_books': num_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def add_book(request):
    data = request.POST
    matching_book = Book.objects.get(isbn=data["isbn"])
    matching_book.users.add(request.user)
    books = Book.objects.filter(users=request.user)
    return render(request, 'stacks/book_list.html'  , {"book_list": [i.title for i in books]})

def book_search_view(request):
    db_update_obj = MaintainBookDatabase()
    db_update_obj.update_book_info(request.GET.get("searched_title"))
    matching_book = Book.objects.filter(title=request.GET.get("searched_title"))
    matching_book = [{"title": i.title, "isbn": i.isbn} for i in matching_book]
    return render(request, 'stacks/book_list_search_result.html'  , {"book_list": matching_book})

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

    print([p.num_books for p in genres])
    trace1 = go.Bar(y=[p.name for p in genres], x=[p.num_books for p in genres], orientation='h')
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
    return render(request, 'stacks/book_agg_hist.html', {"graph": div})