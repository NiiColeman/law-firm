from django.urls import path

from .views import (auth_list, add_auth, authority_update, authority_delete, authority_detail,
                    principle_delete, principle_detail, principle_list, principle_update, tag_list, add_principle
                    )
app_name = "principles"

urlpatterns = [
    path("principles/add-authority",
         add_auth, name="add_authority"),
    path("principles/list-authority",
         auth_list, name="authority_list"),
    path("principles/<int:pk>/update-authority",
         authority_update, name="update_authority"),
    path("principles/<int:pk>/delete-authority",
         authority_delete, name="delete_authority"),
    path("principles/<int:pk>/details",
         authority_detail, name="authority_detail"),

    path("principles/list", principle_list, name="principle_list"),
    path("principles/<int:pk>/detail", principle_detail, name="principle_detail"),
    path("principles/<int:pk>/update", principle_update, name="principle_update"),
    path("principles/<int:pk>/delete", principle_delete, name="principle_delete"),
    path("principles/<int:pk>/tag-list", tag_list, name="tag_list"),
    path("principles/add", add_principle, name="add_principle"),





]
