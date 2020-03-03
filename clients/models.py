from django.db import models

# Create your models here.
from lawyers.models import Lawyer, User
from django.urls import reverse


class ClientCategory(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = 'Client Category'
        verbose_name_plural = 'Client Categories'


class Client(models.Model):
    name = models.CharField(max_length=250)

    phone = models.CharField(max_length=12)
    address = models.TextField()
    email = models.CharField(max_length=150)

    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(ClientCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def get_absolute_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_delete', kwargs={'pk': self.pk})
