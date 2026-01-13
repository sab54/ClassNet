from rest_framework import serializers
from .models import CourseFeedback
from courses.models import Course
from django.contrib.auth import get_user_model

class CourseFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CourseFeedback` model.
    
    This serializer is responsible for converting `CourseFeedback` instances 
    into a format suitable for rendering in responses (like JSON) and for validating 
    input data when creating or updating `CourseFeedback` instances.
    """
    # Nested serializer to get course and user info (optional)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    
    class Meta:
        model = CourseFeedback
        fields = ['id', 'course', 'user', 'rating', 'feedback', 'created_at']
        read_only_fields = ['id', 'created_at']  # These fields should not be editable
