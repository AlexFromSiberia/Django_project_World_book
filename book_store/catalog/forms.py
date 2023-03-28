import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Author, Book


class RenewBookForm(forms.Form):
    """Form for renewing a book."""
    renewal_date = forms.DateField(help_text="Enter date between now and 4 weeks (default value is +3 weeks)")

    def clean_renewal_date(self):
        """Validate the renewal date."""
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data


class AuthorModelForm(forms.ModelForm):
    """Form for creating an author."""
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class BookModelForm(forms.ModelForm):
    """Form for creating a book."""
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
