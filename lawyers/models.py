from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):

    CLERK = 1

    FRONT_DESK = 2

    SECRETARY = 3

    ROLE_CHOICES = (
        (CLERK, 'clerk'),
        (FRONT_DESK, 'front desk'),
        (SECRETARY, 'secretary'),

    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class LawyerStatus(models.Model):
    SENIOR = 1
    JUNIOR = 2

    TYPE_CHOICES = (
        (SENIOR, 'senior'),
        (JUNIOR, 'junior')
    )

    id = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/",null=True, blank=True)
    phone = models.CharField(default="+233 24 4123 456", max_length=50)

    is_lawyer = models.BooleanField(default=False)
    # is_other_staff = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("lawyers:user_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("lawyers:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("lawyers:user_delete", kwargs={"pk": self.pk})


class Lawyer(models.Model):
    """Model definition for Lawyer."""
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bar_number = models.IntegerField(unique=True)
    lawyer_status = models.ForeignKey(
        LawyerStatus, on_delete=models.CASCADE)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Lawyer."""

        verbose_name = 'Lawyer'
        verbose_name_plural = 'Lawyers'

    def __str__(self):
        """Unicode representation of Lawyer."""
        return self.user.username


class OtherStaff(models.Model):
    """Model definition for OtherStaff."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    # TODO: Define fields here

    class Meta:
        """Meta definition for OtherStaff."""

        verbose_name = 'OtherStaff'
        verbose_name_plural = 'OtherStaff'

    def __str__(self):
        """Unicode representation of OtherStaff."""
        return self.user.username

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
