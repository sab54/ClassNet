from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from feedback.models import Course, CourseFeedback
from courses.models import Course
from feedback.forms import CourseFeedbackForm

class CourseFeedbackFormTest(TestCase):

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

    def test_form_valid_data(self):
        """
        Test that the form is valid with correct data.
        """
        form_data = {
            'rating': CourseFeedback.EXCELLENT,
            'feedback': 'This is a fantastic course!'
        }
        form = CourseFeedbackForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())
        # Check if the form's cleaned data is correct
        self.assertEqual(form.cleaned_data['rating'], str(CourseFeedback.EXCELLENT))
        self.assertEqual(form.cleaned_data['feedback'], 'This is a fantastic course!')

    def test_form_invalid_data_missing_feedback(self):
        """
        Test that the form is invalid if the feedback is missing.
        """
        form_data = {
            'rating': CourseFeedback.GOOD,
            'feedback': ''
        }
        form = CourseFeedbackForm(data=form_data)

        # The form should be invalid because feedback is empty
        self.assertFalse(form.is_valid())
        self.assertIn('feedback', form.errors)

    def test_form_invalid_data_invalid_rating(self):
        """
        Test that the form is invalid if an invalid rating is provided.
        """
        form_data = {
            'rating': 6,  # Invalid rating, should be between 1 and 5
            'feedback': 'This course was okay.'
        }
        form = CourseFeedbackForm(data=form_data)

        # The form should be invalid because the rating is outside the valid range
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_saves_data_to_model(self):
        """
        Test that the form correctly saves data to the model when valid.
        """
        form_data = {
            'rating': CourseFeedback.VERY_GOOD,
            'feedback': 'Good course, but could improve in some areas.'
        }
        form = CourseFeedbackForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form and check if the data was saved correctly
        feedback = form.save(commit=False)
        feedback.user = self.user  # Set the user before saving (assume this is required)
        feedback.course = self.course  # Associate with the course
        feedback.save()

        # Verify the data was saved correctly in the model
        saved_feedback = CourseFeedback.objects.get(id=feedback.id)
        self.assertEqual(saved_feedback.rating, CourseFeedback.VERY_GOOD)
        self.assertEqual(saved_feedback.feedback, 'Good course, but could improve in some areas.')
        self.assertEqual(saved_feedback.user, self.user)
        self.assertEqual(saved_feedback.course, self.course)

    def test_rating_field_widget(self):
        """
        Test that the rating field renders as a dropdown.
        """
        form = CourseFeedbackForm()

        # Check if the 'rating' field is rendered as a Select widget (dropdown)
        rating_widget = form.fields['rating'].widget
        self.assertIsInstance(rating_widget, forms.Select)

    def test_feedback_field_widget(self):
        """
        Test that the feedback field renders with the correct widget (Textarea).
        """
        form = CourseFeedbackForm()

        # Check if the 'feedback' field is rendered as a Textarea widget
        feedback_widget = form.fields['feedback'].widget
        self.assertIsInstance(feedback_widget, forms.Textarea)
        self.assertEqual(feedback_widget.attrs['rows'], '10')
        self.assertEqual(feedback_widget.attrs['cols'], '40')


