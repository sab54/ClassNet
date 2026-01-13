from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from courses.models import Course, StudentEnrollment  # Adjust this import according to your model structure
from communication.models import StatusUpdate

class StudentHomeTestCase(TestCase):

    def setUp(self):
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

        # Create users for testing
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,
        )
        
        # Create some courses
        self.course1 = Course.objects.create(name='Course 1', teacher=self.teacher_user, description='Description 1')
        self.course2 = Course.objects.create(name='Course 2', teacher=self.teacher_user, description='Description 2')
        self.course3 = Course.objects.create(name='Course 3', teacher=self.teacher_user, description='Description 3')
        self.course4 = Course.objects.create(name='Course 4', teacher=self.teacher_user, description='Description 4')

        # Enroll student in some courses
        self.enrollment1 = StudentEnrollment.objects.create(course=self.course1, student=self.student_user, progress=50)
        self.enrollment2 = StudentEnrollment.objects.create(course=self.course2, student=self.student_user, progress=75)

        # Create some status updates
        self.status_update1 = StatusUpdate.objects.create(user=self.student_user, content='Status update 1')
        self.status_update2 = StatusUpdate.objects.create(user=self.student_user, content='Status update 2')

    def test_studentHome_logged_in(self):
        # Log the student in
        self.client.login(username='student_user', password='password123')

        # Access the student home page
        response = self.client.get(reverse('student'))

        # Check if the page loads correctly
        self.assertEqual(response.status_code, 200)

        # Check if the enrolled courses are being displayed
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')

        # Check if the available courses are being displayed
        self.assertContains(response, 'Course 3')
        self.assertContains(response, 'Course 4')

        # Check if the student's progress is displayed correctly
        self.assertContains(response, '50')  # Progress of Course 1
        self.assertContains(response, '75')  # Progress of Course 2

        # Check if status updates are displayed
        self.assertContains(response, 'Status update 1')
        self.assertContains(response, 'Status update 2')

    def test_pagination_for_enrolled_courses(self):
        # Log the student in
        self.client.login(username='student_user', password='password123')

        # Create additional enrolled courses to test pagination
        self.course5 = Course.objects.create(name='Course 5', teacher=self.teacher_user, description='Description 5')
        self.enrollment3 = StudentEnrollment.objects.create(course=self.course5, student=self.student_user, progress=90)

        # Access the student home page with pagination
        response = self.client.get(reverse('student') + '?page_enrolled=1')

        # Check if pagination for enrolled courses works
        self.assertEqual(response.status_code, 200)

        # Ensure only 3 courses (due to pagination) are displayed
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')
        self.assertContains(response, 'Course 5')

        # Ensure there are no more than 5 courses per page (pagination of 5)
        enrolled_courses = response.context['page_obj_enrolled']
        self.assertEqual(len(enrolled_courses), 3)  # Adjust this according to the number of enrolled courses

    def test_pagination_for_available_courses(self):
        # Log the student in
        self.client.login(username='student_user', password='password123')

        # Create an additional available course
        self.course6 = Course.objects.create(name='Course 6', teacher=self.teacher_user, description='Description 6')

        # Access the student home page with pagination for available courses
        response = self.client.get(reverse('student') + '?page_available=1')

        # Check if pagination for available courses works
        self.assertEqual(response.status_code, 200)

        # Ensure the available courses are being correctly displayed
        self.assertContains(response, 'Course 3')
        self.assertContains(response, 'Course 4')
        self.assertContains(response, 'Course 6')

        # Ensure there are no more than 5 courses per page (pagination of 5)
        available_courses = response.context['page_obj_available']
        self.assertEqual(len(available_courses), 3)  # Adjust this according to the number of available courses

    def test_no_available_courses(self):
        # Log the student in and ensure they have no available courses
        self.client.login(username='student_user', password='password123')

        # Remove all available courses for the logged-in user
        Course.objects.all().delete()

        # Access the student home page
        response = self.client.get(reverse('student'))

        # Ensure that no available courses are shown
        self.assertNotContains(response, 'Course 3')
        self.assertNotContains(response, 'Course 4')

    def test_status_updates_pagination(self):
        # Log the student in
        self.client.login(username='student_user', password='password123')

        # Create more status updates to test pagination
        self.status_update3 = StatusUpdate.objects.create(user=self.student_user, content='Status update 3')
        self.status_update4 = StatusUpdate.objects.create(user=self.student_user, content='Status update 4')

        # Access the student home page with pagination for status updates
        response = self.client.get(reverse('student') + '?page_status=1')

        # Check if pagination for status updates works
        self.assertEqual(response.status_code, 200)

        # Ensure only 2 status updates (due to pagination) are displayed
        self.assertContains(response, 'Status update 1')
        self.assertContains(response, 'Status update 2')

        # Ensure there are no more than 5 status updates per page (pagination of 5)
        status_updates = response.context['status_page_obj']
        self.assertEqual(len(status_updates), 4)  # Adjust this according to the number of status updates
