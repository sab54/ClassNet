from django.contrib import admin
from .models import Course, StudentEnrollment, CourseMaterial

admin.site.register(Course)
admin.site.register(StudentEnrollment)
admin.site.register(CourseMaterial)
