from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        """String for representing the Model object."""
        return self.name

# Create your models here.
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    class Meta:
        permissions = (("can_view_personal_bookshelf", "view personal bookshelf"),)

    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    users = models.ManyToManyField(User)

    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )

    date_of_pub = models.IntegerField(null = True, blank = True)
    page_num = models.IntegerField(null = True, blank = True)

    genre = models.ForeignKey(Genre, help_text="Select a genre for this book", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    # def get_absolute_url(self):
    #     """Returns the URL to access a detail record for this book."""
    #     return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


