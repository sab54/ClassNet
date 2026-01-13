from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, CourseMaterial, StudentEnrollment, MaterialCompletion

class MarkMaterialAsCompletedTestCase(TestCase):

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

        # Create a material for the course
        self.material = CourseMaterial.objects.create(
            course=self.course,
            description='Test Material',
        )

        # Enroll the student in the course
        self.enrollment = StudentEnrollment.objects.create(
            course=self.course,
            student=self.student_user,
            progress=50
        )

    def test_mark_material_as_completed_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Mark the material as completed via POST request
        response = self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

        # Check if the response is a redirect to the course view page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', kwargs={'course_id': self.course.id}))

        # Verify that the material is marked as completed for the student
        completion = MaterialCompletion.objects.filter(student=self.student_user, material=self.material)
        self.assertEqual(completion.count(), 1)

    def test_mark_material_as_completed_non_authenticated_user(self):
        # Try to mark material as completed without being logged in
        response = self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

        # Ensure that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=' + reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

    def test_mark_material_as_completed_non_enrolled_student(self):
        # Create a student who is not enrolled in the course
        non_enrolled_student = get_user_model().objects.create_user(
            username='non_enrolled_student',
            first_name='Non',
            last_name='Enrolled',
            email='non_enrolled_student@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

        # Log in as the non-enrolled student
        self.client.login(username='non_enrolled_student', password='password123')

        # Try to mark the material as completed
        response = self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))


    def test_mark_material_as_completed_twice(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Mark the material as completed for the first time
        self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

        # Mark the material as completed again (it should toggle the completion status)
        response = self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

        # The second request should delete the previous completion, hence no material should be marked
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', kwargs={'course_id': self.course.id}))

        # Verify that the material completion is deleted
        completion = MaterialCompletion.objects.filter(student=self.student_user, material=self.material)
        self.assertEqual(completion.count(), 0)

    def test_update_progress_on_material_completion(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Total materials count before marking any material as completed
        total_materials = CourseMaterial.objects.filter(course=self.course).count()

        # Mark the material as completed
        self.client.post(reverse('mark_material_as_completed', kwargs={'material_id': self.material.id}))

        # Calculate completed materials
        completed_materials = MaterialCompletion.objects.filter(student=self.student_user, material__course=self.course).count()

        # Update the student's progress
        progress_percentage = (completed_materials / total_materials) * 100

        # Verify the student's progress is updated correctly
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, progress_percentage)

