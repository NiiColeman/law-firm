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


class Room(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class MeetingSession(models.Model):
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False)
    lawyer = models.ForeignKey(
        "lawyers.User", on_delete=models.CASCADE)
    purpose = models.TextField()
    """Model definition for MeetingSession."""
    expired = models.BooleanField(default=False)

    # TODO: Define fields here

    class Meta:
        """Meta definition for MeetingSession."""

        verbose_name = 'Meeting Session'
        verbose_name_plural = 'Meeting Sessions'

    def __str__(self):
        """Unicode representation of MeetingSession."""
        return self.room.name
