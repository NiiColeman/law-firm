from .views import schedule_room, list_schedules, delete_booking, list_sessions, add_session, delete_session
from django.urls import path

app_name = "schedules"

urlpatterns = [


    path('shedules/confrence-room/book', schedule_room, name="add"),

    path('shedules/confrence-room/list', list_schedules, name="list"),


    path('shedules/confrence-room/<int:pk>/delete',
         delete_booking, name="delete"),



    ########################### meetings ########################################
    path('shedules/confrence-room/sessions', list_sessions, name="sessions"),
    path('shedules/confrence-room/add-session',
         add_session, name="add_session"),
    path('shedules/confrence-room/<int:pk>/delete-session',
         delete_session, name="delete_session"),







]
