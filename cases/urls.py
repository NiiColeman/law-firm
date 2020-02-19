from django.urls import path

from .views import (case_list, case_detail, add_case, update_case,
                    delete_case, add_task, AppointmentCreateView, upload_files,
                    new_case, archive_list_view, add_to_archives,
                    archive_detail_view, pending_list, completed_list
                    )


app_name = "cases"


urlpatterns = [



    path("cases/case-list", case_list, name="case_list"),
    path("cases/pending-list", pending_list, name="pending_list"),

    path("cases/completed-list", completed_list, name="completed_list"),

    path("cases/<int:pk>/case-detail", case_detail, name="case_detail"),
    path("cases/add-case", add_case, name="add_case"),
    path("cases/new-case", new_case, name="new_case"),

    path("cases/<int:pk>/case-update", update_case, name="case_update"),
    path("cases/<int:pk>/case-delete", delete_case, name="case_delete"),
    path("cases/tasks/<int:pk>/add-task", add_task, name="add_task"),
    path("cases/files/<int:pk>/add-files", upload_files, name="upload_files"),



    path("cases/appointment/create",
         AppointmentCreateView.as_view(), name='new_appointment'),
    path("cases/archives/list", archive_list_view, name="archive_list"),
    path("cases/archives/<int:pk>/archive-detail",
         archive_detail_view, name="archive_detail"),
    path("cases/archives/<int:pk>/new", add_to_archives, name="archive_new"),




]
