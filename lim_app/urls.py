from django.contrib import admin
from django.urls import path,include
from .views import * 

urlpatterns = [
    path('',home),
    path('home',home),
    path('readers',reader_tab),
    path('save',save_student),
    path('readers/add',save_reader),
    path('readers/edit/<int:id>',edit_reader, name='edit_reader'),
    path('readers/delete/<int:id>',delete_reader, name='delete_reader'),
    path('books', book_tab),
    path('books/add', save_book),
    path('books/edit/<int:id>', edit_book, name='edit_book'),
    path('books/delete/<int:id>', delete_book, name='delete_book'),
    path('books/issue', issue_book, name='issue_book'),
    path('books/issued', view_issued_books, name='view_issued_books'),
    path('books/return/<int:issue_id>', return_book, name='return_book'),
    path('books/lost/<int:issue_id>', mark_as_lost, name='mark_as_lost'),
    path('returns', returns, name='returns'),
]
