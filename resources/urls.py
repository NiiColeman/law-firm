from django.urls import path

from .views import (
    BookListView, add_book, delete_book, add_book, detail_book, book_update,
    request_book, BookHistoryListView, BookHistoryDetailView, HistoryListView, ApproveListView,return_book,
    approve_book
)

app_name = "resources"


urlpatterns = [
    path('books/list', BookListView.as_view(), name='book_list'),

    path('books/<int:pk>/delete', delete_book, name="book_delete"),
    path('books/add_new', add_book, name='book_add'),
    path('books/<int:pk>/book-details', detail_book, name="book_detail"),
    path('books/<int:pk>/update-book', book_update, name="book_update"),
    path('books/<int:pk>/request-book', request_book, name="book_request"),



    ########################################### BOOK REQUESTS ##################################################################
    path('books/request-list', BookHistoryListView.as_view(), name='request_list'),
    path('books/<int:pk>/request-detail',
         BookHistoryDetailView.as_view(), name='request_detail'),
    path('books/<int:pk>/approve-request',
         approve_book, name='approve'),
    ########################################## BOOK APPROVALS #################################################################
    path('books/approved-requests', ApproveListView.as_view(), name='approve_list'),
    path('books/book-history', HistoryListView.as_view(), name='history'),
    path('books/<int:pk>/return-book',return_book, name='return'),

















]
