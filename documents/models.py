from django.db import models
from django.urls import reverse
# Create your models here.


class DocCategory(models.Model):
    """Model definition for Doc Category."""
    title = models.CharField(max_length=250)
    date_updated = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Doc Category."""

        verbose_name = 'Doc Category'
        verbose_name_plural = 'Doc Categories'

    def __str__(self):
        """Unicode representation of Doc Category."""
        return self.title


DOC_CATEGORY_ID = 2


class DocumentStatus(models.Model):
    """Model definition for Status."""
    title = models.CharField(max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Status."""

        verbose_name = 'Document Status'
        verbose_name_plural = 'Document Statuss'

    def __str__(self):
        """Unicode representation of Status."""
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now=False)
    description = models.CharField(
        max_length=550, default='Document Description')
    added_by = models.ForeignKey("lawyers.User", on_delete=models.CASCADE)
    status = models.ForeignKey(
        DocumentStatus, related_name='docstatus', on_delete=models.CASCADE)
    storage_location = models.CharField(max_length=50, default="room 1")
    category = models.ForeignKey(
        DocCategory, default=DOC_CATEGORY_ID, on_delete=models.SET_DEFAULT)

    """Model definition for Document."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Document."""

        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        """Unicode representation of Document."""
        return self.title

    def get_absolute_url(self):
        return reverse("documents:document_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("documents:document_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("documents:document_delete", kwargs={"pk": self.pk})


class DocumentRecord(models.Model):
    """Model definition for AccessedDocument."""
    document = models.ForeignKey(
        Document, related_name='documents', on_delete=models.CASCADE)
    requested_by = models.ForeignKey(
        "lawyers.Lawyer",  on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        "lawyers.OtherStaff", null=True, related_name='staff',on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now=True)
    date_approved = models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Document Record."""

        verbose_name = 'AccessedDocument'
        verbose_name_plural = 'Document Records'

    def __str__(self):
        """Unicode representation of Document Record."""
        return self.document.title

    def get_absolute_url(self):
        return reverse("documents:record_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("documents:record_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("documents:record_delete", kwargs={"pk": self.pk})


    def get_request_url(self):
        return reverse("documents:record_request", kwargs={"pk": self.pk})