from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from users.forms import UserSearchForm
from users.models import CustomUser  # Adjust this import based on your actual model location

class SearchUsersTestCase(TestCase):

    def setUp(self):
        # Create users for testing
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type=CustomUser.TEACHER,
            is_staff=True,
        )
        self.student_user = get_user_model().objects.create_user(
            username='student_user',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password123',
            user_type=CustomUser.STUDENT,
            is_staff=False,
        )
        self.other_teacher = get_user_model().objects.create_user(
            username='another_teacher',
            first_name='Another',
            last_name='Teacher',
            email='another_teacher@example.com',
            password='password123',
            user_type=CustomUser.TEACHER,
            is_staff=True,
        )
        
    def test_teacher_user_search(self):
        # Log in as a teacher user
        self.client.login(username='teacher_user', password='password123')

        # Send a search query that matches a teacher
        response = self.client.post(reverse('search_users'), {'query': 'Teacher'})
        
        # Ensure the response is successful and contains results
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'another_teacher')  # Should return another_teacher user
        self.assertContains(response, 'teacher_user')  # Should return the teacher_user

    def test_non_teacher_user_redirect(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Attempt to search (this should redirect as the user is not a teacher)
        response = self.client.get(reverse('search_users'))
        
        # Check if the user is redirected
        self.assertRedirects(response, '/')
        
        # Check if the error message is present
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You must be a teacher to search for users.", messages)

    def test_empty_search_query(self):
        # Log in as a teacher user
        self.client.login(username='teacher_user', password='password123')

        # Send an empty search query
        response = self.client.post(reverse('search_users'), {'query': ''})

        # Ensure the response is successful and no results are returned
        self.assertEqual(response.status_code, 200)
     
    def test_no_matching_users(self):
        # Log in as a teacher user
        self.client.login(username='teacher_user', password='password123')

        # Send a search query that doesn't match any users
        response = self.client.post(reverse('search_users'), {'query': 'NonExistentUser'})

        # Ensure the response is successful and no results are returned
        self.assertEqual(response.status_code, 200)
    

    def test_search_with_multiple_conditions(self):
        # Log in as a teacher user
        self.client.login(username='teacher_user', password='password123')

        # Search by first name
        response = self.client.post(reverse('search_users'), {'query': 'Teacher'})

        # Ensure the response is successful and contains matching results
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'teacher_user')  # Should return the teacher_user
        self.assertContains(response, 'another_teacher')  # Should return another_teacher user

    def test_invalid_search_form(self):
        # Log in as a teacher user
        self.client.login(username='teacher_user', password='password123')

        # Send invalid data (non-string input like numbers, assuming your form expects a string query)
        response = self.client.post(reverse('search_users'), {'query': '1234'})

        # Ensure the response is successful but may contain validation errors (depending on your form logic)
        self.assertEqual(response.status_code, 200)
