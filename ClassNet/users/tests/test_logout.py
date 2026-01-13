from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session

class LogoutViewTestCase(TestCase):

    def setUp(self):
        # Create a user for testing purposes
        self.user =  get_user_model().objects.create_user(
            username='student_user',
            user_type='student',
            first_name= 'Student',
            last_name= 'Student',
            email= 'student_user@example.com',
            password= 'password123',
            is_staff = False
        )
       
    def test_logout_view_redirects_when_not_logged_in(self):
        """
        Test that an unauthenticated user is redirected to the login page
        when trying to access the logout view.
        """
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/users/login/?next=/users/logout/')
        self.assertEqual(response.status_code, 302)  # Should return a redirect status code

    def test_logout_view_for_logged_in_user(self):
        """
        Test that an authenticated user is logged out and redirected to the login page.
        """
        # Log the user in
        self.client.post(reverse('login'), {'username': 'student_user', 'password': 'password123'})
        response = self.client.get(reverse('logout'))  
        # Test that after logout, the user is redirected to the login page
        self.assertRedirects(response, '/users/login/')
        self.assertEqual(response.status_code, 302)  # Should return a redirect status code
        
