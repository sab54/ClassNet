from django import forms
from .models import Course, CourseMaterial
from communication.models import StatusUpdate
from .models import StudentEnrollment

# Course creation form
class CourseForm(forms.ModelForm):
    """
    Form for creating or updating a `Course` instance.

    This form is used to gather input data from the user when creating or updating a course.
    It includes fields for the course name and description.
    
    Meta:
        model (Course): Specifies that this form is for the `Course` model.
        fields (list): Lists the fields from the model that should be included in the form.
    """
    class Meta:
        model = Course
        fields = ['name', 'description']  # Fields needed for creating a course

# Course material upload form
class CourseMaterialForm(forms.ModelForm):
    """
    Form for uploading course material (e.g., files or resources).

    This form is used to upload files associated with a course. It includes fields for the
    file itself and an optional description of the material.
    
    Meta:
        model (CourseMaterial): Specifies that this form is for the `CourseMaterial` model.
        fields (list): Lists the fields from the model that should be included in the form.
    """
    class Meta:
        model = CourseMaterial
        fields = ['file', 'description']  # Fields for uploading course material

# Enrollment form (Optional, if you want to customize it further)
class EnrollmentForm(forms.Form):
    """
    Form for enrolling a student in a course.

    This form allows a student to select a course from the available courses.
    The form then creates or retrieves an enrollment instance for the selected course.
    
    Methods:
        save(user): Creates or retrieves a `StudentEnrollment` instance for the selected course
        and the provided user (the student).
    """
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Choose Course")

    def save(self, user):
        """
        Save the enrollment for the user (student).

        This method creates or retrieves a `StudentEnrollment` instance for the student
        in the selected course.

        Arguments:
            user: The user (student) who is enrolling in the course.

        Returns:
            enrollment (StudentEnrollment): The `StudentEnrollment` instance for the student.
        """
        # Create a StudentEnrollment instance when a student selects a course
        course = self.cleaned_data['course']
        enrollment, created = StudentEnrollment.objects.get_or_create(course=course, student=user)
        return enrollment




