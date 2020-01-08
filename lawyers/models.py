from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin


from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
      '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
  CLERK = 1
  FRONT DESK = 2
  SECRETARY = 3
 
  ROLE_CHOICES = (
      (CLERK, 'clerk'),
      (FRONT DESK, 'frontdesk'),
      (SECRETARY, 'secretary'),
     
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()


class LawyerStatus(models.Model):
    SENIOR=1
    JUNIOR=2


    TYPE_CHOICES=(
        (SENIOR,'senior'),
        (JUNIOR,'junior')
    )

    id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, primary_key=True)














class User(AbstractUser):
    avatar=models.models.ImageField(upload_to="avatars/")
    
    is_lawyer = models.BooleanField(default=False)
    is_other_staff = models.BooleanField(default=False)
    






class Lawyer(models.Model):
    """Model definition for Lawyer."""
    user=models.OneToOneField("User",on_delete=models.CASCADE)
    bar_number=models.IntegerField()
    lawyer_status=models.ForeignKey(LawyerStatus, verbose_name=_(""), on_delete=models.CASCADE)



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
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role=models.ForeignKey(role on_delete=models.CASCADE)

    # TODO: Define fields here

    class Meta:
        """Meta definition for OtherStaff."""

        verbose_name = 'OtherStaff'
        verbose_name_plural = 'OtherStaffs'

    def __str__(self):
        """Unicode representation of OtherStaff."""
        return self.user.username

        
