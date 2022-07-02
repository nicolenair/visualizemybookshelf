import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SearchBookForm(forms.Form):
    book_name = forms.CharField(help_text="Add a book to shelf")

    def clean_book_name(self):
        data = self.cleaned_data['book_name']
        # Remember to always return the cleaned data.
        return data
