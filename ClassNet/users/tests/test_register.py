from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
    
    def test_registration_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
    
    def test_registration_post_valid(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'user_type': 'student',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Check if the redirect happened
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_registration_post_invalid(self):
        # Invalid data: password mismatch, empty username, missing email
        data = {
            'username': '',  # Empty username
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',  # Invalid email format
            'password': 'password123',
            'confirm_password': 'wrongpassword',  # Password mismatch
            'user_type': 'student',
        }
        response = self.client.post(self.register_url, data)
        
        # Assert that the user was not created
        self.assertFalse(get_user_model().objects.filter(username='').exists())
        self.assertEqual(response.status_code, 200)  # Should return to the same page with errors
        self.assertTemplateUsed(response, 'register.html')
