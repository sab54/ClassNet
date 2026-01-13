from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, StudentEnrollment, CourseMaterial, MaterialCompletion
from django.core.paginator import Paginator, Page

class ViewCourseTestCase(TestCase):

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

        # Create a course and assign it to the teacher
        self.course = Course.objects.create(
            name='Test Course',
            teacher=self.teacher_user,
            description='Course Description',
        )

        # Enroll the student in the course
        self.enrollment = StudentEnrollment.objects.create(
            course=self.course,
            student=self.student_user,
            progress=50,
        )

        # Create course materials
        self.material1 = CourseMaterial.objects.create(
            course=self.course,
            description='Material 1',
        )
        self.material2 = CourseMaterial.objects.create(
            course=self.course,
            description='Material 2',
        )

        # Mark a material as completed by the student
        self.completed_material = MaterialCompletion.objects.create(
            student=self.student_user,
            material=self.material1,
            completed_at='2025-03-03T12:00:00',
        )

    def test_teacher_view_course(self):
        # Log in as the teacher
        self.client.login(username='teacher_user', password='password123')

        # Access the view course page
        response = self.client.get(reverse('view_course', kwargs={'course_id': self.course.id}))

        # Check if the course is being displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Material 1')
        self.assertContains(response, 'Material 2')

        # Check if the enrollments are being displayed
        self.assertContains(response, 'student_user')

        # Check if pagination is working for materials and enrollments
        student_page_obj = response.context['student_page_obj']
        self.assertIsInstance(student_page_obj, Page)

        material_page_obj = response.context['material_page_obj']
        self.assertIsInstance(material_page_obj, Page)

    def test_student_view_course(self):
        # Log in as the student
        self.client.login(username='student_user', password='password123')

        # Access the view course page
        response = self.client.get(reverse('view_course', kwargs={'course_id': self.course.id}))

        # Check if the course is being displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Material 1')
        self.assertContains(response, 'Material 2')

        # Check if the completed materials' IDs are being passed
        self.assertIn(self.material1.id, response.context['completed_material_ids'])
        self.assertNotIn(self.material2.id, response.context['completed_material_ids'])

        # Check if pagination is working for materials
        material_page_obj = response.context['material_page_obj']
        self.assertIsInstance(material_page_obj, Page)


    def test_unauthenticated_user_access(self):
        # Try to access the view course page without being logged in
        response = self.client.get(reverse('view_course', kwargs={'course_id': self.course.id}))

        # Ensure the user is redirected to the login page
        self.assertRedirects(response, '/users/login/?next=' + reverse('view_course', kwargs={'course_id': self.course.id}))

    def test_pagination_for_students_and_materials(self):
        # Log in as the teacher
        self.client.login(username='teacher_user', password='password123')

        # Create more materials to test pagination
        for i in range(10, 21):
            CourseMaterial.objects.create(course=self.course, description=f'Material {i}')

        # Access the view course page with pagination
        response = self.client.get(reverse('view_course', kwargs={'course_id': self.course.id}) + '?student_page=1&material_page=1')

        # Check if pagination for students and materials works correctly
        self.assertEqual(response.status_code, 200)

        # Ensure there are only 5 materials and 5 students displayed per page
        student_page_obj = response.context['student_page_obj']
        self.assertEqual(len(student_page_obj.object_list), 1)  # Adjust based on the enrollments

        material_page_obj = response.context['material_page_obj']
        self.assertEqual(len(material_page_obj.object_list), 5)  # Adjust according to the number of materials

    def test_teacher_not_assigned_course(self):
        # Create a new course assigned to another teacher
        another_teacher_user = get_user_model().objects.create_user(
            username='another_teacher_user',
            first_name='Another Teacher',
            last_name='User',
            email='another_teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,
        )
        another_course = Course.objects.create(
            name='Another Course',
            teacher=another_teacher_user,
            description='Another Course Description',
        )

        # Log in as the teacher who is not assigned to the course
        self.client.login(username='teacher_user', password='password123')

        # Try to access the view page of the course assigned to another teacher
        response = self.client.get(reverse('view_course', kwargs={'course_id': another_course.id}))

        # Ensure the user is redirected to the home page (they should not be able to view the course)
        self.assertRedirects(response, reverse('home'))
