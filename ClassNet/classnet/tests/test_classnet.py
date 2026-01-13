from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

class HomeViewTestCase(TestCase):

    def setUp(self):
        # Create a user (could be a staff user or student based on your use case)
        self.user = get_user_model().objects.create_user(
            username='test_user',
            first_name='Test',
            last_name='User',
            email='test_user@example.com',
            password='password123',
            user_type='student',
            is_staff=False
        )

        # Create 15 courses
        self.courses = []
        for i in range(15):
            course = Course.objects.create(
                name=f'Test Course {i + 1}',
                description=f'Description of Test Course {i + 1}',
                teacher=self.user,
                created_at=f'2025-03-03 10:00:00'
            )
            self.courses.append(course)

    def test_home_view_status_code(self):

        # Access the home page
        response = self.client.get(reverse('home'))

        # Check that the page loads successfully (status code 200)
        self.assertEqual(response.status_code, 200)


    def test_home_view_pagination(self):

        # Access the home page with pagination (first page)
        response = self.client.get(reverse('home') + '?page=1')

        # Check if only 5 courses are displayed
        self.assertEqual(len(response.context['page_obj'].object_list), 6)

        # Ensure that the page contains courses 1 to 6
        for i in range(6):
            self.assertContains(response, f'Test Course {i + 10}')
        # Access the home page with pagination (second page)
        response = self.client.get(reverse('home') + '?page=2')

        # Check if only 5 courses are displayed on the second page
        self.assertEqual(len(response.context['page_obj'].object_list), 6)

        # Ensure that the page contains courses 6 to 10
        for i in range(3, 8):
            self.assertContains(response, f'Test Course {i + 1}')

    def test_home_view_no_courses(self):
        # Delete all courses to simulate no courses available
        Course.objects.all().delete()

        # Access the home page
        response = self.client.get(reverse('home'))

        # Verify that the page contains no courses
        self.assertContains(response, "Want to enroll in a course")  # Ensure your template displays this message when no courses are present
