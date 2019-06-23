from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:pk>/edit/', views.edit_room, name='edit_room'),
    path('room/<int:pk>/sub/', views.subscribe, name='sub'),
    path('room/<int:pk>/unsub/', views.unsubscribe, name='unsub'),
    path('room/<int:pk>/delete/', views.delete, name='delete'),
    path('room/<int:pk>/', views.room, name='room'),
    path('room/new/', views.new_room, name='new_room'),
    path('search/', views.search),
    path('room/<int:pk>/loop/', views.loop),
    path('room/<int:pk>/verificate/', views.verificate),
    path('room/<int:pk>/update/<int:new>/', views.update),
]