from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('update/<int:pk>/', views.event_update, name='event_update'),
    path('delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    path('participants/', views.participant_list, name='participant_list'),
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/update/<int:pk>/', views.participant_update, name='participant_update'),
    path('participants/delete/<int:pk>/', views.participant_delete, name='participant_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
]
