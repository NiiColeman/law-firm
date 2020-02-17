from django.urls import path

from .views import case_list, case_detail, add_case, update_case, delete_case,add_task,AppointmentCreateView


app_name = "cases"


urlpatterns = [



    path("cases/case-list", case_list, name="case_list"),
    path("cases/<int:pk>/case-detail", case_detail, name="case_detail"),
    path("cases/add-case", add_case, name="add_case"),
    path("cases/<int:pk>/case-update", update_case, name="case_update"),
    path("cases/<int:pk>/case-delete", delete_case, name="case_delete"),
    path("cases/tasks/<int:pk>/add-task",add_task,name="add_task"),
    path("cases/appointment/create",AppointmentCreateView.as_view(),name='new_appointment'),


]
