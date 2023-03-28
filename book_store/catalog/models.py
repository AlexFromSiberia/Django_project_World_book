from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Genre model"""
    name = models.CharField(max_length=150,
                            help_text='Enter the book genre',
                            verbose_name='The book genre')

    def __str__(self):
        return self.name


class Language(models.Model):
    """Language model"""
    name = models.CharField(max_length=20,
                            help_text='Enter the book language',
                            verbose_name='The book language')

    def __str__(self):
        return self.name


class Author(models.Model):
    """Author model"""
    first_name = models.CharField(max_length=100,
                                  help_text='Enter author first name',
                                  verbose_name='The author first name')

    last_name = models.CharField(max_length=100,
                                 help_text='Enter author last name',
                                 verbose_name='The author last name')

    date_of_birth = models.CharField(max_length=20,
                                     help_text='Enter date of birth',
                                     verbose_name='Date of birth',
                                     null=True, blank=True)

    date_of_death = models.CharField(max_length=20,
                                     help_text='Enter date of death',
                                     verbose_name='Date of death',
                                     null=True, blank=True)

    def __str__(self):
        return self.last_name


class Book(models.Model):
    """Book model"""
    title = models.CharField(max_length=200,
                             help_text="Enter the title",
                             verbose_name="Book title")
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT,
                              help_text="Choose the genre",
                              verbose_name="The book's genre",
                              null=True)
    language = models.ForeignKey('Language', on_delete=models.PROTECT,
                                 help_text="Choose language",
                                 verbose_name="The book's language", null=True)
    author = models.ManyToManyField('Author',
                                    help_text="Select the author",
                                    verbose_name="Book's author")
    summary = models.TextField(max_length=1000,
                               help_text="Enter a short description",
                               verbose_name="Annotation")
    isbn = models.CharField(max_length=13,
                            help_text="Should be 13 symbols",
                            verbose_name="ISBN of the book")

    def __str__(self):
        return self.title

    def display_author(self):
        """Display the author's last name"""
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Authors'


class Status(models.Model):
    """Status model"""
    name = models.CharField(max_length=20,
                            help_text="Enter the book status",
                            verbose_name="Status of the book")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    """BookInstance model"""
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, )
    inv_num = models.CharField(max_length=20, null=True,
                               help_text="Enter inventory number")
    imprint = models.CharField(max_length=200,
                               help_text="Enter publisher and publish date",
                               verbose_name="Publisher")
    status = models.ForeignKey('Status', on_delete=models.PROTECT,
                               null=True, help_text="Change status",
                               verbose_name="Status of the book")
    due_back = models.DateField(null=True, blank=True,
                                help_text="Enter date of status ending",
                                verbose_name="Status ending date")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.inv_num}, {self.book}, {self.status}"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
