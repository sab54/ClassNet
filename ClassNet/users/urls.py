from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [   
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>', views.user_profile, name='user_profile'),

    # Built-in login and logout views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password Change Views
    path('change_password/', views.change_password, name='change_password'),
    # path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('student/', views.studentHome, name='student'),
    path('teacher/', views.teacherHome, name='teacher'),

    path('search/', views.search_users, name='search_users'),

    path('api/users/', views.CustomUserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<str:username>/', views.CustomUserRetrieveUpdateView.as_view(), name='user-retrieve-update'),

]
