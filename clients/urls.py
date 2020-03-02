from django.urls import path
from .views import client_create_view, client_delete, client_detail, client_list, client_detail, client_update


app_name = 'clients'

urlpatterns = [

    path("clients/client_list", client_list, name='client_list'),
    path("clients/<int:pk>/client-detail", client_detail, name="client_detail"),
    path("clients/<int:pk>/client-update", client_update, name="client_update"),
    path("clients/<int:pk>/client-delete", client_delete, name="client_delete"),
    path("clients/add-client", client_create_view, name="client_add"),



]
