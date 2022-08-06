# Visualize My Bookshelf

Web app for visualizing data about the books a user has read.

Currently supported visualizations:
- distribution of year of publication (histogram)
- bar chart of genre
- distribution of number of pages (histogram)

The application, like any Django application, can be run via python manage.py runserver

When a user uses the search bar to search for a new book to add a new book to their shelf:
- if the book is in the database, it is displayed
- if the book is not in the database, the application searches Wikipedia and Google Books and auto-populates the relevant statistics about that book in the application database.

Then the user, clicks "add book" and the visualizations of the user's bookshelf statistics are auto-updated.

The above functionality works, but here are some things scheduled for improvement:
- improving the automatic information extraction algorithm from Wikipedia and Google Books API.
- increase the number and complexity of supported visualizations
