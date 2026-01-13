from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, StudentEnrollment

class EnrollInCourseTestCase(TestCase):

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

    def test_enroll_in_course_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Enroll in the course via GET request
        response = self.client.get(reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

        # Check if the student is enrolled and redirected to the student dashboard
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('student'))

        # Verify that the enrollment is created in the database
        enrollment = StudentEnrollment.objects.get(course=self.course, student=self.student_user)
        self.assertIsNotNone(enrollment)

    def test_enroll_in_course_non_authenticated_user(self):
        # Try to enroll in a course without being logged in
        response = self.client.get(reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

        # Ensure that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=' + reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

    def test_enroll_in_course_already_enrolled_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Enroll the student in the course
        self.client.get(reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

        # Try to enroll again in the same course
        response = self.client.get(reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

        # The student should not be re-enrolled, and no new enrollment should be created
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('student'))
        
        # Check that only one enrollment exists for this student
        enrollments = StudentEnrollment.objects.filter(course=self.course, student=self.student_user)
        self.assertEqual(enrollments.count(), 1)

    def test_enroll_in_course_non_student_user(self):
        # Log in as a non-student user (e.g., a teacher)
        self.client.login(username='teacher_user', password='password123')

        # Try to enroll in the course
        response = self.client.get(reverse('enroll_in_course', kwargs={'course_id': self.course.id}))

        # The teacher should be redirected to the student dashboard (or a similar place)
        self.assertRedirects(response, reverse('student'))

        # Verify no enrollment for the teacher
        enrollments = StudentEnrollment.objects.filter(course=self.course, student=self.teacher_user)
        self.assertEqual(enrollments.count(), 1)

