from django.contrib import admin

# Register your models here.
from .models import Schedule, Room, MeetingSession

admin.site.register(Schedule)
admin.site.register(Room)
admin.site.register(MeetingSession)
