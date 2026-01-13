from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),
    path('available_courses/', views.available_courses, name='available_courses'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('unenroll/<int:course_id>/', views.unenroll_from_course, name='unenroll_from_course'),
    path('<int:course_id>/add-material/', views.add_material, name='add_material'),
    path('mark_material/<int:material_id>/completed/', views.mark_material_as_completed, name='mark_material_as_completed'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    
    path('teacher/block/<int:course_id>/<int:student_id>/', views.block_student, name='block_student'),
    path('teacher/unblock/<int:course_id>/<int:student_id>/', views.unblock_student, name='unblock_student'),
    path('teacher/remove/<int:course_id>/<int:student_id>/', views.remove_student, name='remove_student'),

    path('notifications/mark_as_read_teacher_notifications/<int:notification_id>/', views.mark_as_read_teacher_notifications, name='mark_as_read_teacher_notifications'),
    path('notifications/mark_as_read_student_notifications/<int:notification_id>/', views.mark_as_read_student_notifications, name='mark_as_read_student_notifications'),

    path('api/courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('api/enrollments/', views.StudentEnrollmentListCreateView.as_view(), name='student-enrollment-list-create'),
    path('api/materials/', views.CourseMaterialListCreateView.as_view(), name='course-material-list-create'),
    path('api/material-completions/', views.MaterialCompletionListCreateView.as_view(), name='material-completion-list-create'),
    path('api/teacher-notifications/', views.TeacherNotificationListCreateView.as_view(), name='teacher-notification-list-create'),
    path('api/student-notifications/', views.StudentNotificationListCreateView.as_view(), name='student-notification-list-create'),
]
