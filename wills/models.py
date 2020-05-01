from django.db import models
from django.urls import reverse
from timezone_field import TimeZoneField
# Create your models here.


class Will(models.Model):
    # client = models.ForeignKey(
    #     "clients.Client", null=True, on_delete=models.SET_NULL)
    client = models.CharField(max_length=250, default="Client Name")
    date_of_execution = models.DateTimeField(auto_now=False)
    date_deposited = models.DateTimeField(auto_now=False)
    receipt_number = models.CharField(max_length=250)
    court = models.CharField(max_length=250)
    internal_depository = models.CharField(max_length=250)
    last_edited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("lawyers.User", null=True,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.client

    def get_absolute_url(self):
        return reverse("wills:details", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("wills:update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("wills:delete", kwargs={"pk": self.pk})

    class Meta:

        verbose_name = 'Will'
        verbose_name_plural = 'Wills'


class AgreementCategory(models.Model):
    title = models.CharField(max_length=250)
    date_modified = models.DateTimeField(auto_now=True)\


    class Meta:

        verbose_name = 'Agreement Category'
        verbose_name_plural = 'Agreement Categories'

    def __str__(self):
        return self.title


class Agreement(models.Model):
    parties = models.CharField(max_length=250)
    # category = models.ForeignKey(
    #     AgreementCategory, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=250, default="")
    date_of_execution = models.DateTimeField(auto_now=False)
    date_of_registration = models.DateTimeField(auto_now=False)

    internal_depository = models.CharField(max_length=250)
    user = models.ForeignKey("lawyers.User", null=True,
                             on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Agreement"
        verbose_name_plural = "Agreements"

    def __str__(self):
        return self.parties
