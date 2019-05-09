from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:pk>/edit/', views.edit_room, name='edit_room'),
    path('room/<int:pk>/', views.room, name='room'),
    path('room/new/', views.new_room, name='new_room')
]