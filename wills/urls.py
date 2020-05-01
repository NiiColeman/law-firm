from django.urls import path
from .views import (will_list, will_detail,
                    will_update,
                    add_will, delete_will, add_agreement,
                    agreement_update, agreement_detail,
                    delete_agreement, agreement_list, cat_detail, cat_list, cat_delete, add_cat, update_cat)

app_name = "wills"


urlpatterns = [
    path('wills/list', will_list, name="will_list"),
    path('will/add', add_will, name='add'),
    path('will/<int:pk>/detail', will_detail, name='details'),
    path('will/<int:pk>/update', will_update, name='update'),
    path('will/<int:pk>/deletee', delete_will, name='delete'),
    ###################################### AGREEMENTS ###################################
    path('agreements/list', agreement_list, name="agreement_list"),
    path('agreements/<int:pk>/detail', agreement_detail, name='agreement_detail'),
    path('agreements/<int:pk>/update', agreement_update, name='agreement_update'),
    path('agreements/<int:pk>/delete', delete_agreement, name='agreement_delete'),
    path('agreements/add', add_agreement, name='add_agreement'),

    #################################### ARGREEMENT CATEGORY ############################
    path("wills/categroy/<int:pk>/category-details",
         cat_detail, name="cat_detail"),
    path("wills/categroy/<int:pk>/category-update",
         update_cat, name="cat_update"),
    path("wills/categroy/<int:pk>/category-delete",
         cat_delete, name="cat_delete"),
    path("wills/categroy/add-category", add_cat, name="cat_add"),
    path("wills/categroy/list", cat_list, name="cat_list"),














]
