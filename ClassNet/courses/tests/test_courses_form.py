from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Course, StudentEnrollment, CourseMaterial, MaterialCompletion, TeacherNotification, StudentNotification
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

class CourseFormTestCase(TestCase):

    def test_course_creation(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )

        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )

        self.assertEqual(course.name, "Math 101")
        self.assertEqual(course.description, "Basic Math Course")
        self.assertEqual(course.teacher, teacher)
        self.assertIsInstance(course.created_at, timezone.datetime)

    def test_str_method(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )

        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )

        self.assertEqual(str(course), "Math 101")


class StudentEnrollmentFormTestCase(TestCase):

    def test_student_enrollment(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        student = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            first_name='Student',
            last_name='One',
            user_type='student',
            is_staff=False,
        )

        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )

        enrollment = StudentEnrollment.objects.create(
            course=course,
            student=student,
            progress=50.00
        )

        self.assertEqual(enrollment.course, course)
        self.assertEqual(enrollment.student, student)
        self.assertEqual(enrollment.progress, 50.00)
        self.assertIsInstance(enrollment.enrolled_at, timezone.datetime)

    def test_unique_together_constraint(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,  # Ensure the user is a staff
        )
        student = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            first_name='Student',
            last_name='One',
            user_type='student',
            is_staff=False,
        )
        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )

        # Create first enrollment
        StudentEnrollment.objects.create(
            course=course,
            student=student,
            progress=50.00
        )


class CourseMaterialFormTestCase(TestCase):

    def test_course_material_creation(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )

        material = CourseMaterial.objects.create(
            course=course,
            file=None,  # Assuming no file is uploaded during this test
            description="Lecture Notes for Math 101"
        )

        self.assertEqual(material.course, course)
        self.assertEqual(material.description, "Lecture Notes for Math 101")
        self.assertIsInstance(material.uploaded_at, timezone.datetime)

    def test_str_method(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )
        material = CourseMaterial.objects.create(
            course=course,
            file=None,
            description="Lecture Notes for Math 101"
        )
        self.assertEqual(str(material), "Material for Math 101")


class MaterialCompletionFormTestCase(TestCase):

    def test_material_completion_creation(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        student = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            first_name='Student',
            last_name='One',
            user_type='student',
            is_staff=False,
        )
        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )
        material = CourseMaterial.objects.create(
            course=course,
            file=None,
            description="Lecture Notes for Math 101"
        )
        completion = MaterialCompletion.objects.create(
            student=student,
            material=material
        )

        self.assertEqual(completion.student, student)
        self.assertEqual(completion.material, material)
        self.assertIsInstance(completion.completed_at, timezone.datetime)

    def test_unique_together_constraint(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        student = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            first_name='Student',
            last_name='One',
            user_type='student',
            is_staff=False,
        )
        course = Course.objects.create(
            name="Math 101",
            description="Basic Math Course",
            teacher=teacher
        )
        material = CourseMaterial.objects.create(
            course=course,
            file=None,
            description="Lecture Notes for Math 101"
        )
        # Create first completion
        MaterialCompletion.objects.create(
            student=student,
            material=material
        )


class TeacherNotificationFormTestCase(TestCase):

    def test_teacher_notification_creation(self):
        teacher = get_user_model().objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='password123',
            first_name='Teacher',
            last_name='One',
            user_type='teacher',
            is_staff=True,
        )
        notification = TeacherNotification.objects.create(
            teacher=teacher,
            message="New material has been uploaded."
        )

        self.assertEqual(notification.teacher, teacher)
        self.assertEqual(notification.message, "New material has been uploaded.")
        self.assertIsInstance(notification.date_created, timezone.datetime)
        self.assertFalse(notification.is_read)


class StudentNotificationFormTestCase(TestCase):

    def test_student_notification_creation(self):
        notification = StudentNotification.objects.create(
            message="You have a new course assignment."
        )

        self.assertEqual(notification.message, "You have a new course assignment.")
        self.assertIsInstance(notification.date_created, timezone.datetime)
        self.assertFalse(notification.is_read)

