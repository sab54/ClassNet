from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/feedback/', views.course_feedback, name='course_feedback'),
    path('api/feedback/', views.CourseFeedbackListCreateView.as_view(), name='course-feedback-list-create'),
]
