from rest_framework import serializers
from .models import Course, StudentEnrollment, CourseMaterial, MaterialCompletion, TeacherNotification, StudentNotification
from django.contrib.auth import get_user_model

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Course` model.

    This serializer is used to convert the `Course` model instances into a format
    that can be easily rendered into JSON, XML, or other content types. It also validates
    incoming data when creating or updating a course.

    Fields:
        id (IntegerField): The unique identifier of the course.
        name (CharField): The name of the course.
        description (TextField): A detailed description of the course.
        teacher (PrimaryKeyRelatedField): The teacher associated with the course (represented by the teacher's ID).
        created_at (DateTimeField): The timestamp when the course was created.

    Meta:
        model (Course): Specifies that this serializer works with the `Course` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    teacher = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'teacher', 'created_at']
        read_only_fields = ['id', 'created_at']


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the `StudentEnrollment` model.

    This serializer is used to convert `StudentEnrollment` model instances into a format
    that can be rendered into JSON or other content types. It also validates the incoming
    data when creating or updating a student's enrollment in a course.

    Fields:
        id (IntegerField): The unique identifier for the enrollment.
        course (PrimaryKeyRelatedField): The course in which the student is enrolled, represented by the course's ID.
        student (PrimaryKeyRelatedField): The student who is enrolled in the course, represented by the student's ID.
        progress (DecimalField): The student's progress in the course (as a percentage).
        blocked (BooleanField): Indicates whether the student's enrollment is blocked or not.
        enrolled_at (DateTimeField): The timestamp when the student enrolled in the course.

    Meta:
        model (StudentEnrollment): Specifies that this serializer works with the `StudentEnrollment` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    
    class Meta:
        model = StudentEnrollment
        fields = ['id', 'course', 'student', 'progress', 'blocked', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at']


class CourseMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CourseMaterial` model.

    This serializer is used to convert `CourseMaterial` model instances into a format
    that can be rendered into JSON or other content types. It also validates the incoming
    data when creating or updating materials related to a course.

    Fields:
        id (IntegerField): The unique identifier for the course material.
        course (PrimaryKeyRelatedField): The course to which the material belongs, represented by the course's ID.
        file (FileField): The file associated with the course material (e.g., lecture notes, assignments).
        description (CharField): A brief description of the material (e.g., title or content summary).
        uploaded_at (DateTimeField): The timestamp when the material was uploaded.

    Meta:
        model (CourseMaterial): Specifies that this serializer works with the `CourseMaterial` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = CourseMaterial
        fields = ['id', 'course', 'file', 'description', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class MaterialCompletionSerializer(serializers.ModelSerializer):
    """
    Serializer for the `MaterialCompletion` model.

    This serializer is used to convert `MaterialCompletion` model instances into a format
    that can be rendered into JSON or other content types. It also validates the incoming
    data when creating or updating materials related to a course.

    Fields:
        id (IntegerField): The unique identifier for the course material.
        course (PrimaryKeyRelatedField): The course to which the material belongs, represented by the course's ID.
        file (FileField): The file associated with the course material (e.g., lecture notes, assignments).
        description (CharField): A brief description of the material (e.g., title or content summary).
        uploaded_at (DateTimeField): The timestamp when the material was uploaded.

    Meta:
        model (MaterialCompletion): Specifies that this serializer works with the `MaterialCompletion` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    material = serializers.PrimaryKeyRelatedField(queryset=CourseMaterial.objects.all())
    
    class Meta:
        model = MaterialCompletion
        fields = ['id', 'student', 'material', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class TeacherNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the `TeacherNotification` model.

    This serializer is used to convert `TeacherNotification` model instances into a format
    that can be rendered into JSON or other content types. It also validates the incoming
    data when creating or updating materials related to a course.

    Fields:
        id (IntegerField): The unique identifier for the course material.
        course (PrimaryKeyRelatedField): The course to which the material belongs, represented by the course's ID.
        file (FileField): The file associated with the course material (e.g., lecture notes, assignments).
        description (CharField): A brief description of the material (e.g., title or content summary).
        uploaded_at (DateTimeField): The timestamp when the material was uploaded.

    Meta:
        model (TeacherNotification): Specifies that this serializer works with the `TeacherNotification` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    
    teacher = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(is_staff=True))
    
    class Meta:
        model = TeacherNotification
        fields = ['id', 'teacher', 'message', 'date_created', 'is_read']
        read_only_fields = ['id', 'date_created']


class StudentNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the `StudentNotification` model.

    This serializer is used to convert `StudentNotification` model instances into a format
    that can be rendered into JSON or other content types. It also validates the incoming
    data when creating or updating materials related to a course.

    Fields:
        id (IntegerField): The unique identifier for the course material.
        course (PrimaryKeyRelatedField): The course to which the material belongs, represented by the course's ID.
        file (FileField): The file associated with the course material (e.g., lecture notes, assignments).
        description (CharField): A brief description of the material (e.g., title or content summary).
        uploaded_at (DateTimeField): The timestamp when the material was uploaded.

    Meta:
        model (StudentNotification): Specifies that this serializer works with the `StudentNotification` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    # No student field here because it's not defined in the model
    class Meta:
        model = StudentNotification
        fields = ['id', 'message', 'date_created', 'is_read']
        read_only_fields = ['id', 'date_created']
