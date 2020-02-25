from django.db import models

# Create your models here.


class Authority(models.Model):
    """Model definition for Authority."""
    title = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Authority."""

        verbose_name = 'Authority'
        verbose_name_plural = 'Authorities'

    def __str__(self):
        """Unicode representation of Authority."""
        return self.title


class Principles(models.Model):
    """Model definition for Principles."""
    principle = models.CharField(max_length=350)
    authority = models.ManyToManyField(Authority)
    description = models.TextField(default="")

    added_by = models.ForeignKey(
        "lawyers.User", null=True,  on_delete=models.SET_NULL)
    date_add = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Principles."""

        verbose_name = 'Principles'
        verbose_name_plural = 'Principles'

    def __str__(self):
        """Unicode representation of Principles."""
        return self.principle
