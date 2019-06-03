from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:pk>/edit/', views.edit_room, name='edit_room'),
    path('room/<int:pk>/sub/', views.subscribe, name='sub'),
    path('room/<int:pk>/unsub/', views.unsubscribe, name='unsub'),
    path('room/<int:pk>/delete/', views.delete, name='delete'),
    path('room/<int:pk>/', views.room, name='room'),
    path('room/new/', views.new_room, name='new_room'),
    re_path(r'^search/$', views.search),
]