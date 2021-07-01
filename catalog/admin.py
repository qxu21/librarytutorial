from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "born")
    # order fields. tupling in this list puts them horizontally on the same row
    fields = ["first_name", "last_name", ("born", "died")]
    inlines = [BooksInline]
    # exclude = ['died']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class BooksInstanceInline(admin.TabularInline):
    # TabularInline lays out horizontally
    # StackedInline does it vertically
    model = BookInstance

    # for some reason it creates placeholders if you don't do this
    extra = 0


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "due_back", "short_id")
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    # you can put method names in here.
    # set method.short_description for a name to be rendered
    # to admin interface
    list_display = ("title", "author")

    inlines = [BooksInstanceInline]
