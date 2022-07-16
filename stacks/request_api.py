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
        search_url = title
        search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
        search_json = json.loads(search_response)
        
        if len(search_json[3])>1:
            search_url = title + " book"
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        if len(search_json[3]) < 1:
            search_url = title + " novel"
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        if len(search_json[3]) < 1:
            search_url = title
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        print(search_json[3])
        html_doc = requests.get(search_json[3][0]).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        title_url = re.search("(.*?) - Wikipedia" , soup.find_all('head')[0].title.get_text()).group(1)
        response = requests.get(f"https://en.wikipedia.org//w/api.php?action=query&format=json&prop=revisions&titles={title_url}&formatversion=2&rvprop=content&rvslots=*")

        google_books_response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={title}")
        google_books_response = json.loads(google_books_response.text)

        for i, e in enumerate(google_books_response["items"]):
            if "authors" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "description" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "categories" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "pageCount" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            author = google_books_response["items"][i]["volumeInfo"]["authors"][0]
            summary = google_books_response["items"][i]["volumeInfo"]["description"]
            genre = google_books_response["items"][i]["volumeInfo"]["categories"][0] #tmp
            page_num = google_books_response["items"][i]["volumeInfo"]["pageCount"] #tmp
            isbn = google_books_response["items"][i]["volumeInfo"]["industryIdentifiers"][0]["identifier"]

            break

        country_pub = re.search("country\s*=\s*\[*\[*([\w, \.]+)\]*\]*", response.text)
        if country_pub:
            country_pub = country_pub.group(1)
            
        date_pub = re.search("[s|S]hort description\s*\|\s*(\d\d\d\d)", response.text)
        if date_pub is not None:
            date_pub = date_pub.group(1)

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
                    country_pub = Book._meta.get_field('country_of_pub').get_default()
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

            if page_num is None:
                page_num = Book._meta.get_field('page_num').get_default()

            if summary is None:
                summary = Book._meta.get_field('summary').get_default()

            if isbn is not None: #do not create books with no isbn
                self.create_book(title, author, page_num, country_pub, date_pub, summary, genre, isbn)


    def convert_title_url(self, title):
        return re.sub(" ", "%20", title)

    def create_book(self, title, author, page_num, country_pub, date_pub, summary, genre, isbn):
        b = Book(title=title, author=author, date_of_pub=date_pub, page_num=page_num, country_of_pub=country_pub, summary=summary, genre=genre, isbn=isbn)
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