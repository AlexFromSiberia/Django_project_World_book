from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance


class AuthorAdmin (admin.ModelAdmin):
    """Author admin interface"""
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


class BookInstanceInline(admin.TabularInline):
    """BookInstance admin interface"""
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    """Book admin interface"""
    list_display = ('title', 'genre', 'language', 'display_author', 'id')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    """BookInstance admin interface"""
    list_display = ('borrower', 'book', 'inv_num', 'imprint', 'status', 'due_back', 'id')
    list_filter = ('book', 'status', )
    fieldsets = (
        ('The book', {'fields': ('book', 'inv_num', 'imprint')}),
        ('Status',   {'fields': ('status', 'due_back', 'borrower',)}),
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
