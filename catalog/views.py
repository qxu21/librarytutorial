import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    genre_counts = {}

    for g in Genre.objects.all():
        genre_counts[g.name] = Book.objects.filter(genre__name__exact=g.name).count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "genre_counts": genre_counts,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    # WARNING: generic templates are expected in
    # app/templates/app/model_list.html
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="c")
            .order_by("due_back")
        )


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Lists all loaned books to staff members"""

    model = BookInstance
    permission_required = "catalog.view_all"
    template_name = "catalog/bookinstance_list_checked_out.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="c").order_by("due_back")


@login_required
@permission_required("catalog.manage_status", raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("borrowed"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


# CreateView and UpdateView expect modelname_form.html
class AuthorCreate(PermissionRequiredMixin, CreateView):

    # default perms created for model are
    # add_model, change_model, delete_model, update_model
    permission_required = "catalog.add_author"
    model = Author
    fields = ["first_name", "last_name", "born", "died"]
    initial = {"died": "11/06/2020"}

    # if desired:
    # template_name_suffix = '_other_suffix'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = "catalog.change_author"
    model = Author
    fields = (
        "__all__"  # Not recommended (potential security issue if more fields added)
    )


# DeleteView expects modelname_confirm_delete.html
class AuthorDelete(PermissionRequiredMixin, DeleteView):

    permission_required = "catalog.delete_author"
    model = Author
    success_url = reverse_lazy("authors")
