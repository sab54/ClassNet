
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm

class UserLoginTestCase(TestCase):

    def setUp(self):
        self.user_teacher = get_user_model().objects.create_user(
            username='teacher_user',
            user_type='teacher',
            first_name= 'Teacher',
            last_name= 'Teacher',
            email= 'teacher_user@example.com',
            password= 'password123',
            is_staff = True
        )
        self.user_student = get_user_model().objects.create_user(
            username='student_user',
            user_type='student',
            first_name= 'Student',
            last_name= 'Student',
            email= 'student_user@example.com',
            password= 'password123',
            is_staff = False
        )

    def test_login_teacher(self):
        response = self.client.post(reverse('login'), {'username': 'teacher_user', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertRedirects(response, reverse('teacher'))  # Teacher should be redirected to teacher page

    def test_login_student(self):
        response = self.client.post(reverse('login'), {'username': 'student_user', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertRedirects(response, reverse('student'))  # Student should be redirected to student page

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'invalid_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertContains(response, 'Invalid username or password')
