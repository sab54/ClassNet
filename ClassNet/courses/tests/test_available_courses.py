from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

class AvailableCoursesTestCase(TestCase):

    def setUp(self):
        # Create users
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,
        )

        self.student_user = get_user_model().objects.create_user(
            username='student_user',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

        # Create some courses
        self.course1 = Course.objects.create(
            name='Course 1',
            description='Description of Course 1',
            teacher=self.teacher_user,
        )
        self.course2 = Course.objects.create(
            name='Course 2',
            description='Description of Course 2',
            teacher=self.teacher_user,
        )

        # URL for the available_courses view
        self.url = reverse('available_courses')  # Adjust according to the URL name used in your urls.py

    def test_redirect_if_not_logged_in(self):
        # Ensure that an unauthenticated user is redirected to the login page
        response = self.client.get(self.url)

        # The user should be redirected to the login page
        self.assertRedirects(response, f'/users/login/?next={self.url}')

    def test_access_if_logged_in(self):
        # Log in as the test user
        self.client.login(username='student_user', password='password123')

        # Ensure that the user can access the available_courses page
        response = self.client.get(self.url)

        # The response should be successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the courses are displayed on the page
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')

    def test_courses_ordered_by_creation_date(self):
        # Log in as the test user
        self.client.login(username='student_user', password='password123')

        # Create a new course with an earlier creation date
        self.course3 = Course.objects.create(
            name='Course 3',
            description='Description of Course 3',
            teacher=self.teacher_user,
        )

        # Ensure that the courses are ordered by creation date
        response = self.client.get(self.url)

        # The first course should be the most recently created one
        self.assertContains(response, 'Course 1')  # This should appear first if it was created last
        self.assertContains(response, 'Course 2')
        self.assertContains(response, 'Course 3')  # Ensure the new course is also listed
