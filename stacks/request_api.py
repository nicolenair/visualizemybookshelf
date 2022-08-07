from bs4 import BeautifulSoup
import requests
import json
import re 
from stacks.models import Book, Author, Genre, Place
from stacks.information_extraction.bert_information_extraction import InformationExtractor

# brute force
# update list of books in db
# for each book in list, check if it is already in db, 
#   if it is, check if info matches api
    # update info where necessary   

class MaintainBookDatabase:
    def __init__(self):
        self.information_extractor = InformationExtractor()

    def __call__(self):
        self.update_book_list()

        for book_title in self.book_list:
            self.update_book_info(book_title)

    def update_book_list(self):
        self.book_list = ["Beowulf", "Thinking, Fast and Slow", "Good Omens", "Anne of Green Gables"]

    def update_book_info_neural(self, title):
        google_books_response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={title}")
        google_books_response = json.loads(google_books_response.text)

        for i, e in enumerate(google_books_response["items"]):
            if "title" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if not google_books_response["items"][i]["volumeInfo"]["title"].replace(" ", "").isascii():
                continue
            if "authors" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "description" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "categories" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "pageCount" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            if "industryIdentifiers" not in google_books_response["items"][i]["volumeInfo"]:
                continue
            author = google_books_response["items"][i]["volumeInfo"]["authors"][0]
            summary = google_books_response["items"][i]["volumeInfo"]["description"]
            genre = google_books_response["items"][i]["volumeInfo"]["categories"][0] #tmp
            page_num = google_books_response["items"][i]["volumeInfo"]["pageCount"] #tmp
            isbn = google_books_response["items"][i]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
            title_google_normalized = google_books_response["items"][i]["volumeInfo"]["title"] #tmp
            break

        print("TITLE ", title_google_normalized, "ISBN", isbn)

        search_url = title_google_normalized
        search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
        search_json = json.loads(search_response)

        if len(search_json[3])>1:
            search_url = title_google_normalized + " book"
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        if len(search_json[3]) < 1:
            search_url = title_google_normalized + " novel"
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        if len(search_json[3]) < 1:
            search_url = title_google_normalized
            search_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_url}&format=json").text
            search_json = json.loads(search_response)

        html_doc = requests.get(search_json[3][0]).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        text = soup.findAll('p')

        full_text = ""
        count = 0
        for i in text:
            if len(i.text)>5:
                full_text += i.text + ". "
                count += 1
            if count > 1:
                break


        text = full_text
        # for i in text:
        #     if len(i.text) > 5:
        #         text = i.text
        #         break

        # else:
        #     text = text[0].text

        date_pub = self.information_extractor(f"In what year was it originally published?", text)
        if date_pub == "[CLS]":
            date_pub = self.information_extractor(f"What is the year of the book?", text)
        if date_pub == "[CLS]":
            date_pub = self.information_extractor(f"What is the year?", text)

        date_pub = re.search("(\d\d\d\d)", date_pub).group(1)

        if not Book.objects.filter(isbn=isbn).exists():
            if not Author.objects.filter(name=author).exists():
                if  author is not None:
                    author = self.create_author(author)
                else:
                    author = Book._meta.get_field('author').get_default()
            else:
                author = Author.objects.filter(name=author)[0]

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

            if isbn is not None: #do not create books with no isbn $ and len(Genre.objects.filter(name=title))==0
                self.create_book(title_google_normalized, author, page_num, date_pub, summary, genre, isbn)
                return isbn

        return isbn

    def convert_title_url(self, title):
        return re.sub(" ", "%20", title)

    def create_book(self, title, author, page_num, date_pub, summary, genre, isbn):
        b = Book(title=title, author=author, date_of_pub=date_pub, page_num=page_num, summary=summary, genre=genre, isbn=isbn)
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