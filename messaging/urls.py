from django.urls import path
from . import views

# Author: Student 3 - Tawfiq

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:pk>/', views.view_message, name='view_message'),
    path('delete/<int:pk>/', views.delete_message, name='delete_message'),
]