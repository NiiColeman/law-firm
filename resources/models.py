from django.db import models
from django.urls import reverse

# Create your models here.


class Branch(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=250)
    date_added = models.DateField(auto_now=False)
    date_modified = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    added_by = models.ForeignKey(
        "lawyers.OtherStaff", null=True, on_delete=models.SET_NULL)
    shelf_number = models.CharField(max_length=250)
    requested = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse("resources:book_detail", kwargs={"pk": self.pk})

    def get_update_url(self):

        return reverse("resources:book_update", kwargs={"pk": self.pk})

    def get_delete_url(self):

        return reverse("resources:book_delete", kwargs={"pk": self.pk})

    def get_request_url(self):

        return reverse("resources:book_request", kwargs={"pk": self.pk})


class BookHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(
        'lawyers.Lawyer', null=True, on_delete=models.SET_NULL)
    date_requested = models.DateField(auto_now=False)
    approved_by = models.ForeignKey(
        'lawyers.OtherStaff', null=True, on_delete=models.SET_NULL)
    returned = models.BooleanField(default=False)
    approved=models.BooleanField(default=False)
    date_approved = models.DateField(auto_now=False,null=True)

    date_returned = models.DateField(auto_now=False,null=True,blank=True)

    def __str__(self):
        return self.book.title

    def get_absolute_url(self):

        return reverse("resources:history_detail", kwargs={"pk": self.pk})

    def get_update_url(self):

        return reverse("resources:history_update", kwargs={"pk": self.pk})

    def get_delete_url(self):

        return reverse("resources:history_delete", kwargs={"pk": self.pk})
