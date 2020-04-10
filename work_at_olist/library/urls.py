from django.urls import path
from library import views

urlpatterns = [
     path('authors/', views.AuthorList.as_view(), name='authors-list'),
]