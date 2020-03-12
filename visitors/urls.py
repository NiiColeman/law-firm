from django.urls import path
from .views import visitor_detail, visitor_list, add_visitor, delete_visitor, update_visitor


app_name = "visitors"


urlpatterns = [
    path("visitors/add", add_visitor, name="add"),
    path('visitors/update/<int:pk>/visitor',
         update_visitor, name="visitor_update"),
    path('visitors/delete/<int:pk>/visitor', delete_visitor, name="delete"),
    path('visitors/detail/<int:pk>/visitor',
         visitor_detail, name="visitor_detail"),
    path('visitors/list', visitor_list, name="visitor_list"),




]
