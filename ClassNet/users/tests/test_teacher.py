from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from courses.models import Course, StudentEnrollment
from communication.models import StatusUpdate

class TeacherHomeTestCase(TestCase):

    def setUp(self):
        # Create a student and a teacher user
        self.student_user = get_user_model().objects.create_user(
            username='student_user',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

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

    def test_teacherHome_logged_in(self):
        # Log the teacher in
        self.client.login(username='teacher_user', password='password123')

        # Access the teacher home page
        response = self.client.get(reverse('teacher'))

        # Check if the page loads correctly
        self.assertEqual(response.status_code, 200)

        # Check if the teacher's courses are being displayed
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')
        self.assertContains(response, 'Course 3')
        self.assertContains(response, 'Course 4')

        # Check if the students enrolled in the courses are displayed
        self.assertContains(response, 'student_user')

    def test_pagination_for_teacher_courses(self):
        # Log the teacher in
        self.client.login(username='teacher_user', password='password123')

        # Create additional courses to test pagination
        self.course5 = Course.objects.create(name='Course 5', teacher=self.teacher_user, description='Description 5')
        self.course6 = Course.objects.create(name='Course 6', teacher=self.teacher_user, description='Description 6')

        # Access the teacher home page with pagination
        response = self.client.get(reverse('teacher') + '?page=1')

        # Check if pagination for courses works
        self.assertEqual(response.status_code, 200)

        # Ensure only 5 courses (due to pagination) are displayed
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')
        self.assertContains(response, 'Course 3')
        self.assertContains(response, 'Course 4')
        self.assertContains(response, 'Course 5')

        # Ensure there are no more than 5 courses per page
        courses = response.context['page_obj_course']
        self.assertEqual(len(courses), 6)  # Adjust this according to your pagination settings

    def test_no_courses_for_teacher(self):
        # Log the teacher in and ensure they have no courses
        self.client.login(username='teacher_user', password='password123')
    
        # Remove all courses for the logged-in teacher
        courses=Course.objects.all().delete()
   
        # Access the teacher home page
        response = self.client.get(reverse('teacher'))

        # Ensure that no courses are shown
        self.assertNotContains(response, 'Course 3')
        self.assertNotContains(response, 'Course 4')

    def test_students_enrolled_in_courses(self):
        # Log the teacher in
        self.client.login(username='teacher_user', password='password123')

        # Access the teacher home page
        response = self.client.get(reverse('teacher'))

        # Check if the students enrolled in each course are being displayed
        self.assertContains(response, 'student_user')  # Ensure the enrolled student is displayed

    def test_course_enrollment_display(self):
        # Log the teacher in
        self.client.login(username='teacher_user', password='password123')

        # Access the teacher home page
        response = self.client.get(reverse('teacher'))

        # Check if the enrollment data is being correctly displayed
        self.assertContains(response, 'Description 1')
        self.assertContains(response, 'Description 2')
        self.assertContains(response, 'Description 3')
        self.assertContains(response, 'Description 4')
