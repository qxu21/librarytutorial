import uuid
from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Book Genre")

    class Meta:
        # metadata here
        # can put '-' before a parameter to sort in reverse order
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)

    # default on_delete is models.CASCADE, deleting all books by an author
    # when an author is deleted. PROTECT or RESTRICT prevents author deletion
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    language = models.CharField(max_length=50, blank=True, default="English")
    published = models.IntegerField()

    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Builtin to define a URL to this resource"""
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    # imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("c", "Checked out"),
        ("a", "Available"),
        ("h", "On hold"),
    )
    # values are shown to users, keys are saved

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]

        # perms go in here! perms are associated with models!
        permissions = (
            ("view_all", "Can view all books"),
            ("manage_status", "Can check out and renew books"),
        )

    def short_id(self):
        return str(self.id)[0:6]

    short_id.short_description = "ID"

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    born = models.DateField(null=True, blank=True)
    died = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
