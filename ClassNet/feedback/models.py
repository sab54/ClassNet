# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from courses.models import Course
from django.conf import settings

class CourseFeedback(models.Model):
    """
    Model to represent feedback for a course. This includes a rating, detailed feedback,
    and a relationship to both the course and the user providing the feedback.
    """
    # Define rating choices
    EXCELLENT = 1
    VERY_GOOD = 2
    GOOD = 3
    BAD = 4
    VERY_BAD = 5
    
    RATING_CHOICES = [
        (EXCELLENT, 'Excellent'),
        (VERY_GOOD, 'Very Good'),
        (GOOD, 'Good'),
        (BAD, 'Bad'),
        (VERY_BAD, 'Very Bad'),
    ]
    
    # ForeignKey to the Course model (Assuming you have a Course model in your 'courses' app)
    course = models.ForeignKey(Course, related_name='feedback_set', on_delete=models.CASCADE)
    
    # ForeignKey to the User model. It uses `settings.AUTH_USER_MODEL` to refer to the user model dynamically.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Rating field using the choices defined above
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=EXCELLENT)
    
    # A text field to hold detailed feedback
    feedback = models.TextField()
    
    # Auto-generated timestamp for when the feedback is created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the model for ease of identification
    def __str__(self):
        return f"Feedback for {self.course.name} by {self.user.username}"

    # Optionally, add validation for the rating field
    def clean(self):
        if self.rating not in dict(self.RATING_CHOICES):
            raise ValidationError("Rating must be between 1 and 5.")
