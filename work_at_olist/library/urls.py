from django.urls import path
from library import views

urlpatterns = [
     path('authors/', views.AuthorList.as_view(), name='authors-list'),
     path('books/', views.BookList.as_view(), name='books-list'),
     path('books/<int:pk>/', views.BookDetail.as_view(), name='books-detail'),
]
