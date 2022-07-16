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
        self.book_list = ["Beowulf", "Thinking, Fast and Slow", "Good Omens", "Anne of Green Gables"]

    def update_book_info(self, title):
        title_url = self.convert_title_url(title)
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={title_url}")
        response = json.loads(response.text)

        for i, e in enumerate(response["items"]):
            if "industryIdentifiers" in response["items"][i]["volumeInfo"]:
                author = response["items"][i]["volumeInfo"]["authors"][0] #tmp
                date_pub = response["items"][i]["volumeInfo"]["publishedDate"].split("-")[0]
                summary = response["items"][i]["volumeInfo"]["description"]
                isbn = response["items"][i]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                genre = response["items"][i]["volumeInfo"]["categories"][0] #tmp
                page_num = response["items"][i]["volumeInfo"]["pageCount"]
                break

        if not Book.objects.filter(title=title).exists():
            if not Author.objects.filter(name=author).exists():
                if  author is not None:
                    author = self.create_author(author)
                else:
                    author = Book._meta.get_field('author').get_default()
            else:
                author = Author.objects.filter(name=author)[0]
            # if not Place.objects.filter(name=country_pub).exists():
            #     if  country_pub is not None:
            #         country_pub = self.create_place(country_pub)
            #     else:
            #         country_pub = Book._meta.get_field('place_of_pub').get_default()
            # else:
            #     country_pub = Place.objects.filter(name=country_pub)[0]

            

            if not Genre.objects.filter(name=genre).exists():
                if  genre is not None:
                    genre = self.create_genre(genre)
                else:
                    genre = Book._meta.get_field('genre').get_default()
            else:
                genre = Genre.objects.filter(name=genre)[0]

            if page_num is None:
                page_num = Book._meta.get_field('page_num').get_default()

            if date_pub is None:
                date_pub = Book._meta.get_field('date_of_pub').get_default()

            if summary is None:
                summary = Book._meta.get_field('summary').get_default()

            if isbn is not None: #do not create books with no isbn
                self.create_book(title, author, page_num, date_pub, summary, genre, isbn)

    def convert_title_url(self, title):
        return re.sub(" ", "%20", title)

    def create_book(self, title, author, page_num, date_pub, summary, genre, isbn):
        b = Book(title=title, author=author, page_num=page_num, date_of_pub=date_pub, summary=summary, genre=genre, isbn=isbn)
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