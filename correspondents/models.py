from django.db import models
from django.urls import reverse
# Create your models here.


class Correspondent(models.Model):
    """Model definition for Correspondent."""
    title = models.CharField(max_length=250)
    case = models.ForeignKey('cases.Case', null=True,
                             blank=True, on_delete=models.SET_NULL)
    clients = models.ForeignKey('clients.Client', null=True,
                                blank=True, on_delete=models.SET_NULL)
    correspondent = models.CharField(max_length=250)

    date_added = models.DateTimeField(auto_now=False)
    lawyer = models.ForeignKey(
        'lawyers.User', null=True, on_delete=models.SET_NULL)
    description = models.TextField()

    # TODO: Define fields here

    class Meta:
        """Meta definition for Correspondent."""

        verbose_name = 'Correspondent'
        verbose_name_plural = 'Correspondents'

    def __str__(self):
        """Unicode representation of Correspondent."""
        return self.title

    def get_absolute_url(self):

        return reverse("correspondents:detail", kwargs={"pk": self.pk})

    def get_update_url(self):

        return reverse("correspondents:update", kwargs={"pk": self.pk})

    def get_delete_url(self):

        return reverse("correspondents:delete", kwargs={"pk": self.pk})

    # TODO: Define custom methods here
