from django.urls import path
from . import views

urlpatterns = [
    path('status_update', views.add_status_update, name='add_status_update'),
    path('api/status_updates/', views.status_update_list, name='status_update_list'),  # API for GET/POST
]