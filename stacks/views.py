from django.shortcuts import render
from stacks.models import Book, User
from django.contrib.auth.mixins import PermissionRequiredMixin
from stacks.request_api import MaintainBookDatabase
import plotly.graph_objects as go
import plotly.offline as opy
from django.contrib.auth.decorators import permission_required, login_required

from .models import Book, Genre, Place
from django.db.models import Count, Q, F, Case, When
# Create your views here.
from django.views import generic

@login_required
def view_all_books(request):
    books = Book.objects.filter(users=request.user)
    return render(request, 'stacks/book_list.html', {"book_list": [{"title": i.title, "author": i.author} for i in books]})

@login_required
def add_book(request):
    data = request.POST
    matching_book = Book.objects.get(isbn=data["isbn"])
    matching_book.users.add(request.user)
    books = Book.objects.filter(users=request.user)
    return render(request, 'stacks/book_list.html'  , {"book_list": [{"title": i.title, "author": i.author} for i in books]})

def book_search_view(request):
    db_update_obj = MaintainBookDatabase()
    isbn = db_update_obj.update_book_info_neural(request.GET.get("searched_title"))
    matching_book = Book.objects.filter(isbn=isbn)

    print("matching", matching_book, isbn)
    matching_book = [{"title": i.title, "isbn": i.isbn, "author": i.author} for i in matching_book]
    return render(request, 'stacks/book_list_search_result.html'  , {"book_list": matching_book})

@login_required
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

@login_required
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

@login_required
def book_genre_agg(request):
    genres = Genre.objects.annotate(num_books=Count(Case(
        When(book__users=request.user, then=1))))

    genres = [i for i in genres if i.num_books > 0]
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
    figure.update_xaxes(tick0=1, dtick=1)

    div = opy.plot(figure, auto_open=False, output_type='div')
    return render(request, 'stacks/book_agg_hist.html', {"graph": div})