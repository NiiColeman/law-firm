from django.db import models
from django.urls import reverse
from timezone_field import TimeZoneField
from django.core.exceptions import ValidationError
# Create your models here.


class Category(models.Model):
    """Model definition for Category."""
    name = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def get_absolute_url(self):
        return reverse("cases:category_detail", kwargs={"pk": self.pk})

    # TODO: Define custom methods here


class Status(models.Model):
    """Model definition for Status."""
    title = models.CharField(max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Status."""

        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        """Unicode representation of Status."""
        return self.title

    def get_absolute_url(self):
        return reverse("cases:status_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:status_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("cases:status_delete", kwargs={"pk": self.pk})


DEFAULT_STATUS_ID = 2


class Case(models.Model):
    name = models.CharField(max_length=350)
    description = models.TextField()
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    lawyer = models.ManyToManyField("lawyers.Lawyer")
    client = models.ForeignKey(
        "clients.Client", null=True, on_delete=models.SET_NULL)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now=False)
    status = models.ForeignKey(
        Status, default=DEFAULT_STATUS_ID, on_delete=models.CASCADE)
    court = models.CharField(default='District Court', max_length=250)
    # attachments = models.ForeignKey(
    #     Attachment, null=True, on_delete=models.SET_NULL)

    added_by = models.ForeignKey("lawyers.user", on_delete=models.CASCADE)

    """Model definition for Case."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Case."""

        verbose_name = 'Case'
        verbose_name_plural = 'Cases'

    def __str__(self):
        """Unicode representation of Case."""
        return self.name

    def get_absolute_url(self):
        return reverse("cases:case_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:case_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("cases:case_delete", kwargs={"pk": self.pk})


class CaseFile(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=250)
    file = models.FileField(upload_to="attachments/")
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for CaseFile."""

        verbose_name = 'Case File'
        verbose_name_plural = 'Case Files'

    def __str__(self):
        """Unicode representation of CaseFile."""
        return self.case.name


class PriorityLevel(models.Model):
    """Model definition for PriorityLevel."""
    priority = models.CharField(max_length=250)

    # TODO: Define fields here

    class Meta:
        """Meta definition for PriorityLevel."""

        verbose_name = 'PriorityLevel'
        verbose_name_plural = 'PriorityLevels'

    def __str__(self):
        """Unicode representation of PriorityLevel."""
        return self.priority


class CaseTask(models.Model):
    """Model definition for CaseTask."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.CharField(max_length=250)
    description = models.TextField()
    date_modefied = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(auto_now=False)
    priority_level = models.ForeignKey(
        PriorityLevel, null=True, on_delete=models.SET_NULL)
    complete = models.BooleanField(default=False)

    # TODO: Define fields here

    class Meta:
        """Meta definition for CaseTask."""

        verbose_name = 'Case Task'
        verbose_name_plural = 'Case Tasks'

    def __str__(self):
        """Unicode representation of CaseTask."""
        return self.task


class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='UTC')

    # Additional fields not visible to users
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('view_appointment', args=[str(self.id)])

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        appointment_time = arrow.get(self.time, self.time_zone.zone)

        if appointment_time < arrow.utcnow():
            raise ValidationError(
                'You cannot schedule an appointment for the past. '
                'Please check your time and time_zone')


class CaseArchive(models.Model):
    """Model definition for CaseArchives."""
    case = models.OneToOneField(Case, null=True, on_delete=models.SET_NULL)
    archived_by = models.ForeignKey(
        "lawyers.OtherStaff", null=True, on_delete=models.SET_NULL)
    # date_archived = models.DateTimeField(auto_now=False)
    date_modefied = models.DateTimeField(auto_now=True)
    archive_location = models.CharField(max_length=250, default="Archives")

    # TODO: Define fields here

    class Meta:
        """Meta definition for CaseArchives."""

        verbose_name = 'CaseArchives'
        verbose_name_plural = 'CaseArchives'

    def __str__(self):
        """Unicode representation of CaseArchive."""
        return self.case.name

    def get_absolute_url(self):
        return reverse("cases:archive_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:archive_update", kwargs={"pk": self.pk})


class LegalArgument(models.Model):
    argument = models.CharField(max_length=350, unique=True)
    authorities = models.TextField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.argument

    class Meta:

        verbose_name = 'LegalArgument'
        verbose_name_plural = 'LegalArguments'
