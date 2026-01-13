from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Course
from feedback.models import CourseFeedback
from django.core.exceptions import ValidationError
from datetime import datetime

class CourseFeedbackModelTest(TestCase):

    def setUp(self):
        """
        Set up the necessary data for testing.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password',
            user_type='teacher',
            is_staff=True,  # Ensure the user is a staff
        )

        # Create a course
        self.course = Course.objects.create(
            name='Test Course',
            description='A test course',
            teacher=self.user
        )



    def test_course_feedback_creation(self):
        """
        Test the creation of a CourseFeedback object.
        """
        feedback = CourseFeedback.objects.create(
            course=self.course,
            user=self.user,
            rating=CourseFeedback.EXCELLENT,
            feedback="This is a great course!"
        )

        # Check if the feedback was created successfully
        self.assertEqual(feedback.course, self.course)
        self.assertEqual(feedback.user, self.user)
        self.assertEqual(feedback.rating, CourseFeedback.EXCELLENT)
        self.assertEqual(feedback.feedback, "This is a great course!")
        self.assertTrue(isinstance(feedback.created_at, datetime))  # created_at should be a datetime object

    def test_rating_validation_valid(self):
        """
        Test that valid ratings do not raise a validation error.
        """
        valid_ratings = [CourseFeedback.EXCELLENT, CourseFeedback.VERY_GOOD, CourseFeedback.GOOD, 
                         CourseFeedback.BAD, CourseFeedback.VERY_BAD]
        
        for rating in valid_ratings:
            feedback = CourseFeedback(
                course=self.course,
                user=self.user,
                rating=rating,
                feedback="This is a great course!"
            )
            try:
                feedback.clean()  # This should not raise any errors
            except ValidationError:
                self.fail(f"ValidationError raised for valid rating: {rating}")

    def test_rating_validation_invalid(self):
        """
        Test that invalid ratings raise a ValidationError.
        """
        invalid_rating = 6  # Ratings should be between 1 and 5
        feedback = CourseFeedback(
            course=self.course,
            user=self.user,
            rating=invalid_rating,
            feedback="This is a great course!"
        )
        with self.assertRaises(ValidationError):
            feedback.clean()  # This should raise a ValidationError

    def test_str_method(self):
        """
        Test the string representation of the CourseFeedback model.
        """
        feedback = CourseFeedback.objects.create(
            course=self.course,
            user=self.user,
            rating=CourseFeedback.EXCELLENT,
            feedback="This is a great course!"
        )

        expected_str = f"Feedback for {self.course.name} by {self.user.username}"
        self.assertEqual(str(feedback), expected_str)

    def test_feedback_foreignkey_course(self):
        """
        Test the foreign key relationship with the Course model.
        """
        feedback = CourseFeedback.objects.create(
            course=self.course,
            user=self.user,
            rating=CourseFeedback.EXCELLENT,
            feedback="This is a great course!"
        )
        self.assertEqual(feedback.course.name, 'Test Course')
        
    def test_feedback_foreignkey_user(self):
        """
        Test the foreign key relationship with the User model.
        """
        feedback = CourseFeedback.objects.create(
            course=self.course,
            user=self.user,
            rating=CourseFeedback.EXCELLENT,
            feedback="This is a great course!"
        )
        self.assertEqual(feedback.user.username, 'testuser')
