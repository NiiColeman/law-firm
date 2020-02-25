from django.urls import path

from .views import (case_detail, add_case, update_case,
                    delete_case, add_task, AppointmentCreateView, upload_files,
                    new_case, archive_list_view, add_to_archives,
                    archive_detail_view, pending_list, completed_list, CaseList, CaseCreateView, CategoryListView,
                    delete_cat, cat_update, cat_add, add_argument, cat_detail, file_list,
                    delete_files, task_view

                    )


app_name = "cases"


urlpatterns = [

    path('cases/list/', CaseList.as_view(), name='case_list'),



    path("cases/pending-list", pending_list, name="pending_list"),

    path("cases/completed-list", completed_list, name="completed_list"),

    path("cases/<int:pk>/case-detail", case_detail, name="case_detail"),
    path("cases/add-case", add_case, name="add_case"),



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


    path("cases/category/list", CategoryListView.as_view(), name="cat_list"),
    path("cases/category/<int:pk>/update",
         cat_update, name="cat_update"),
    path("cases/category/<int:pk>/delete", delete_cat, name="cat_delete"),
    path("cases/category/add", cat_add, name="cat_add"),
    path("cases/argument/<int:pk>/add", add_argument, name="add_arg"),
    path("cases/category/<int:pk>/detail", cat_detail, name="cat_detail"),
    path("cases/<int:pk>/case-files", file_list, name="file_list"),
    path("cases/<int:pk>/delete_file", delete_files, name="delete_file"),
    path("cases/tasks/<int:pk>/list", task_view, name="task_list"),







]
