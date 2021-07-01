from django.urls import path
from . import views

urlpatterns = [
    # name makes it reversible, for example can link from other spots
    # such as <a href="{% url 'index' %}">Home</a>.
    path("", views.index, name="index"),
    # a class-based view so we can use inheritance
    path("books/", views.BookListView.as_view(), name="books"),
    # <int:pk> captures an integer parameter as pk.
    # the generic list view will expect an integer parameter NAMED pk!
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    # you can use re_path(re,view,**kwargs) for regex!
    # remember to use r'string' in python
    # third positional arg to path is a dict passed as kwargs to the view function
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path("checkedout/", views.LoanedBooksListView.as_view(), name="borrowed"),
    path(
        "book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"
    ),
    path("author/create/", views.AuthorCreate.as_view(), name="author-create"),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author-update"),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author-delete"),
]
