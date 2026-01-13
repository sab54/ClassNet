# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, CourseFeedback
from .forms import CourseFeedbackForm
from rest_framework import generics
from .serializers import CourseFeedbackSerializer

class CourseFeedbackListCreateView(generics.ListCreateAPIView):
    """
    API View for listing and creating course feedback.
    
    This view provides two main functionalities:
    1. It allows listing all the feedbacks submitted for courses (GET request).
    2. It allows submitting new feedback for a course (POST request).
    """
    queryset = CourseFeedback.objects.all()
    serializer_class = CourseFeedbackSerializer

    def perform_create(self, serializer):
        # Optionally, you can associate the feedback with the current user.
        # serializer.save(user=self.request.user)
        serializer.save()

def course_feedback(request, course_id):
    """
    View to handle displaying and submitting feedback for a specific course.
    
    This view provides the following functionalities:
    1. Displays existing feedback for the given course.
    2. Allows users to submit new feedback for the course (only if they are authenticated).
    """
    # Get the specific course based on the provided ID
    course = get_object_or_404(Course, id=course_id)
    
    # Handle the form submission
    if request.method == 'POST':
        form = CourseFeedbackForm(request.POST)
        if form.is_valid():
            # Associate the feedback with the current course and the logged-in user
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user  # Set the current user as the author
            feedback.save()
            return redirect('course_feedback', course_id=course.id)  # Redirect to the same page
    
    else:
        form = CourseFeedbackForm()
    
    # Get the feedback for the logged-in user
    feedbacks = course.feedback_set.filter(user=request.user)
    
    # Render the template with the form and course feedback
    return render(request, 'feedback_form.html', {
        'form': form,
        'course': course,
        'feedbacks': feedbacks,  # Pass existing feedback to the template
    })


