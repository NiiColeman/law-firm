from django.db import models
from django.urls import reverse
# Create your models here.


class Visitor(models.Model):
    """Model definition for Visitor."""
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=250)
    purpose = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now=True)
    address = models.TextField()
    # TODO: Define fields here

    class Meta:
        """Meta definition for Visitor."""

        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'

    def __str__(self):
        """Unicode representation of Visitor."""
        return self.name

    def get_absolute_url(self):
        return reverse("visitors:visitor_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("visitors:visitor_update", kwargs={"pk": self.pk})
