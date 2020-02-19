from django.urls import path
from .views import (document_detail, document_list, record_detail, record_list, update_document,
                    add_document, record_list,
                    document_request,
                    document_request_list,
                    document_delete_view, request_doc, record_update, record_delete, approve_request, document_archive_list, record_archive_list

                    )


app_name = 'documents'

urlpatterns = [
    path("documents/document-list", document_list, name="doc_list"),
    path('documents/<int:pk>/document-detail',
         document_detail, name='document_detail'),
    path('documents/<int:pk>/document-delete',
         document_delete_view, name='document_delete'),
    path('documents/<int:pk>/document-update',
         update_document, name='document_update'),
    path('documents/requests/<int:pk>/document-request',
         request_doc, name='record_request'),
    path('documents/add-document', add_document, name="add_document"),
    path('documents/records/list', record_list, name='record_list'),
    path('documents/records/<int:pk>/detail',
         record_detail, name='record_detail'),
    path('documents/records/<int:pk>/update',
         record_update, name='record_update'),
    path('documents/records/<int:pk>/delete',
         record_delete, name='record_delete'),

    path('documents/requests/add-request',
         document_request, name='add_request'),
    path('documents/requests/record-list',
         document_request_list, name='request_list'),
    path('documents/requests/<int:pk>/approve',
         approve_request, name='approve'),

    path("doccuments/archives", document_archive_list, name="doc_archives"),
    path("doccuments/record-archives", record_archive_list, name="rec_archives"),




]
