from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
]
