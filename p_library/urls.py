from django.contrib import admin
from django.urls import path
from .views import AuthorDelete, AuthorEdit, AuthorList, AuthorCreateMany, BooksAuthorsCreateMAny, FriendUpdate, Friends, FriendDelete, FriendCreate

app_name = 'p_library'
urlpatterns = [
    path('author/create/', AuthorEdit.as_view(), name='author_create'),
    path('author/', AuthorList.as_view(), name='authors_list'),
    path('author/create_many/', AuthorCreateMany, name='author_create_many'),
    path('author_book/create_many/', BooksAuthorsCreateMAny, name='author_book_create_many'),
    path('author/delete/', AuthorDelete, name='author_delete'),
    path('friend/', Friends, name='friend_list'),
    path('friend/create/', FriendCreate.as_view(), name='friend_create'),
    path('friend/delete/', FriendDelete, name='friend_delete'),
    path('friend/edit/<int:pk>/', FriendUpdate.as_view(), name='friend_update'),
]