from .views import schedule_room, list_schedules, delete_booking
from django.urls import path

app_name = "schedules"

urlpatterns = [


    path('shedules/confrence-room/book', schedule_room, name="add"),
    path('shedules/confrence-room/list', list_schedules, name="list"),
    path('shedules/confrence-room/<int:pk>/delete',
         delete_booking, name="delete"),






]
