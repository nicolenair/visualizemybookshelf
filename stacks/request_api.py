from bs4 import BeautifulSoup
import requests
import json
import re 
from stacks.models import Book, Author, Genre, Place
# brute force
# update list of books in db
# for each book in list, check if it is already in db, 
#   if it is, check if info matches api
    # update info where necessary   

class MaintainBookDatabase:
    def __call__(self):
        self.update_book_list()

        for book_title in self.book_list:
            self.update_book_info(book_title)

    def update_book_list(self):
        self.book_list = ["Good Omens"]

    def update_book_info(self, title):
        title_url = self.convert_title_url(title)
        response = requests.get(f"https://en.wikipedia.org//w/api.php?action=query&format=json&prop=revisions&titles={title_url}&formatversion=2&rvprop=content&rvslots=*")
        author = re.search("author[\(*s\)*]*\s*=\s*\[*\[*([\w, \.]+)\]*\]*", response.text)
        if author:
            author = author.group(1)
        country_pub = re.search("country\s*=\s*\[*\[*([\w, \.]+)\]*\]*", response.text)
        if country_pub:
            country_pub = country_pub.group(1)
            
        date_pub = re.search("release_date\s*=\s*.*?(\d+).*?\|", response.text)
        if date_pub:
            date_pub = date_pub.group(1)

        summary = re.search("{{Short description\|(.*?)}}", response.text)
        if summary:
            summary = summary.group(1)

        isbn = re.search("isbn\s*=\s*.*?([\d, -]+[X]*).*?\|", response.text)

        if isbn:
            isbn = isbn.group(1)


        genre = "tbd"
        # if genre:
        #     genre = genre.group(1)


        if not Book.objects.filter(title=title).exists():
            if not Author.objects.filter(name=author).exists():
                if  author is not None:
                    author = self.create_author(author)
                else:
                    author = Book._meta.get_field('author').get_default()
            else:
                author = Author.objects.filter(name=author)[0]
            if not Place.objects.filter(name=country_pub).exists():
                if  country_pub is not None:
                    country_pub = self.create_place(country_pub)
                else:
                    country_pub = Book._meta.get_field('place_of_pub').get_default()
            else:
                country_pub = Place.objects.filter(name=country_pub)[0]

            if not Genre.objects.filter(name=genre).exists():
                if  genre is not None:
                    genre = self.create_genre(genre)
                else:
                    genre = Book._meta.get_field('genre').get_default()
            else:
                genre = Genre.objects.filter(name=genre)[0]

            if date_pub is None:
                date_pub = Book._meta.get_field('date_of_pub').get_default()

            if summary is None:
                summary = Book._meta.get_field('summary').get_default()

            if isbn is not None: #do not create books with no isbn
                self.create_book(title, author, country_pub, date_pub, summary, genre, isbn)

    def convert_title_url(self, title):
        return re.sub(" ", "%20", title)

    def create_book(self, title, author, country_pub, date_pub, summary, genre, isbn):
        b = Book(title=title, author=author, place_of_pub=country_pub, date_of_pub=date_pub, summary=summary, genre=genre, isbn=isbn)
        b.save()
        return b

    def create_author(self, name):
        b = Author(name=name)
        b.save()
        return b

    def create_place(self, name):
        b = Place(name=name)
        b.save()
        return b

    def create_genre(self, name):
        b = Genre(name=name)
        b.save()
        return b