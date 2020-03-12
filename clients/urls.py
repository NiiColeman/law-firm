from django.urls import path
from .views import (client_create_view, client_delete,
                    client_detail, client_list,
                    client_detail, client_update,
                    cat_delete, cat_detail,
                    category_list, add_cat,
                    update_cat,
                    client_cat,

                    )


app_name = 'clients'

urlpatterns = [

    path("clients/client_list", client_list, name='client_list'),
    path("clients/<int:pk>/client-detail", client_detail, name="client_detail"),
    path("clients/<int:pk>/client-update", client_update, name="client_update"),
    path("clients/<int:pk>/client-delete", client_delete, name="client_delete"),
    path("clients/add-client", client_create_view, name="client_add"),

    path("clients/categroy/<int:pk>/category-details",
         cat_detail, name="cat_detail"),
    path("clients/categroy/<int:pk>/category-update",
         update_cat, name="cat_update"),
    path("clients/categroy/<int:pk>/category-delete",
         cat_delete, name="cat_delete"),
    path("clients/categroy/add-category", add_cat, name="cat_add"),
    path("clients/categroy/list", category_list, name="cat_list"),
    path("clients/clients/categroy/<int:pk>/list",
         client_cat, name="client_cat"),

    #     path('')




]
