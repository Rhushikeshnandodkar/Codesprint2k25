from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('create-room', views.create_room, name='create-room'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('questionsdash/<int:room_id>', views.questionsdash, name='questionsdash'),
    path('room-details/<int:room_id>', views.room_details, name='room_details'),
]