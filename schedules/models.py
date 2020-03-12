from django.db import models

# Create your models here.


class Schedule(models.Model):
    user = models.ForeignKey('lawyers.User', null=True,
                             on_delete=models.SET_NULL)
    # day = models.DateTimeField()
    purpose = models.CharField(max_length=250)
    end_time = models.DateTimeField(auto_now=False)
    expired = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.purpose

    class Meta:

        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
