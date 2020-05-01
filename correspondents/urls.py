from django.urls import path
from .views import list_corrs, add_corrs, detail_corrs, delete_corrs, update_corrs, case_corrs, case_add_corrs


app_name = "correspondents"


urlpatterns = [
    path('correspondents/list', list_corrs, name="list"),
    path('correspondents/<int:pk>/list', case_corrs, name="case-list"),

    path('correspondents/<int:pk>/details', detail_corrs, name="detail"),
    path('correspondents/<int:pk>/update', update_corrs, name="update"),
    path('correspondents/<int:pk>/delete', delete_corrs, name="delete"),
    path('correspondents/add', add_corrs, name="add"),
    path('correspondents/<int:pk>/add', case_add_corrs, name="case_add"),






]
