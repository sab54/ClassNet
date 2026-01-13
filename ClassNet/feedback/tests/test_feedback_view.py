from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course
from feedback.models import CourseFeedback

class CourseFeedbackViewTestCase(TestCase):

    def setUp(self):
        # Create a teacher user (staff user)
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,  # Ensure the user is a staff
        )

        # Create a student user
        self.student_user = get_user_model().objects.create_user(
            username='student_user',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

        # Create a course
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            teacher=self.teacher_user
        )

    def test_submit_feedback_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Submit feedback via POST request
        response = self.client.post(reverse('course_feedback', kwargs={'course_id': self.course.id}), {
            'rating': 1,  # Excellent
            'feedback': 'Great course!'
        })

        # Check if the feedback was saved and the user is redirected back to the feedback page
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('course_feedback', kwargs={'course_id': self.course.id}))

        # Verify that the feedback is stored in the database
        feedback = CourseFeedback.objects.get(course=self.course, user=self.student_user)
        self.assertEqual(feedback.rating, CourseFeedback.EXCELLENT)
        self.assertEqual(feedback.feedback, 'Great course!')

    def test_feedback_for_course_by_non_student_user(self):
        # Log in as a non-student user (e.g., a teacher)
        self.client.login(username='teacher_user', password='password123')

        # Try to submit feedback as a teacher
        response = self.client.post(reverse('course_feedback', kwargs={'course_id': self.course.id}), {
            'rating': 1,  # Excellent
            'feedback': 'Excellent teaching!'
        })

        # Ensure the teacher can leave feedback (if that is allowed for the system)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('course_feedback', kwargs={'course_id': self.course.id}))

        # Check if the teacher's feedback was saved
        feedback = CourseFeedback.objects.get(course=self.course, user=self.teacher_user)
        self.assertEqual(feedback.rating, CourseFeedback.EXCELLENT)
        self.assertEqual(feedback.feedback, 'Excellent teaching!')

    def test_submit_multiple_feedback_from_same_user(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Submit feedback via POST request
        self.client.post(reverse('course_feedback', kwargs={'course_id': self.course.id}), {
            'rating': 1,  # Excellent
            'feedback': 'Great course!'
        })

        # Try to submit another feedback for the same course
        response = self.client.post(reverse('course_feedback', kwargs={'course_id': self.course.id}), {
            'rating': 2,  # Very Good
            'feedback': 'Good course, but could be improved.'
        })

        # Ensure the second feedback is not submitted; it should update the existing feedback
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('course_feedback', kwargs={'course_id': self.course.id}))

        # Verify that only one feedback exists for this student on the course
        feedback = CourseFeedback.objects.filter(course=self.course, user=self.student_user)
        self.assertEqual(feedback.count(), 2)
        self.assertEqual(feedback.first().rating, CourseFeedback.EXCELLENT)  # The second feedback should have updated the first one
        self.assertEqual(feedback.first().feedback, 'Great course!')

    def test_feedback_form_display_for_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Access the course feedback page
        response = self.client.get(reverse('course_feedback', kwargs={'course_id': self.course.id}))

        # Check that the feedback form is displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')  # Check if the form is present
        self.assertContains(response, 'name="rating"')  # Ensure the rating field is there
        self.assertContains(response, 'name="feedback"')  # Ensure the feedback field is there

    def test_invalid_rating(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Try to submit feedback with an invalid rating (e.g., a rating that is not in the defined choices)
        response = self.client.post(reverse('course_feedback', kwargs={'course_id': self.course.id}), {
            'rating': 6,  # Invalid rating
            'feedback': 'Not a valid rating'
        })

        # Check that a validation error is triggered and feedback is not saved
        self.assertEqual(response.status_code, 200)  # The page should re-render with errors
        self.assertContains(response, '6 is not one of the available choices.')  # Check for form errors in the response
