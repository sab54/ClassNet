from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from users.forms import UserUpdateForm
from django.contrib.messages import get_messages

class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user_teacher = get_user_model().objects.create_user(
            username='teacher_user',
            user_type='teacher',
            first_name='Teacher',
            last_name='Teacher',
            email='teacher_user@example.com',
            password='password123',
            is_staff=True            
        )
        self.user_student = get_user_model().objects.create_user(
            username='student_user',
            user_type='student',
            first_name='Student',
            last_name='Student',
            email='student_user@example.com',
            password='password123',
            is_staff=False
        )

    def test_profile_teacher_redirect(self):
        self.client.login(username='teacher_user', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Teacher should be able to access their profile
        self.assertContains(response, 'Profile')  # You can check if "Profile" exists in the page content

    def test_profile_student_redirect(self):
        self.client.login(username='student_user', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Student should be able to access their profile
        self.assertContains(response, 'Profile')  # Similarly check for profile text

    def test_profile_update_teacher(self):
        self.client.login(username='teacher_user', password='password123')
        response = self.client.post(reverse('profile'), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'username':'teacher_user',
            'user_type':'teacher',
            'password':'password123',
            'is_staff':True, 
        })
        self.user_teacher.refresh_from_db()  # Refresh user object to get updated data
        self.assertEqual(response.status_code, 302)  # Should redirect after profile update
        self.assertRedirects(response, reverse('teacher'))  # Should redirect to teacher page
        self.assertEqual(self.user_teacher.first_name, 'NewFirstName')  # Check if the update worked
        self.assertEqual(self.user_teacher.last_name, 'NewLastName')  # Check if the update worked
        self.assertEqual(self.user_teacher.email, 'newemail@example.com')  # Check if the update worked

    def test_profile_update_student(self):
        self.client.login(username='student_user', password='password123')
        response = self.client.post(reverse('profile'), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'username':'student_user',
            'user_type':'student',
            'password':'password123',
            'is_staff':False,
        })
        self.user_student.refresh_from_db()  # Refresh user object to get updated data
        self.assertEqual(response.status_code, 302)  # Should redirect after profile update
        self.assertRedirects(response, reverse('student'))  # Should redirect to student page
        self.assertEqual(self.user_student.first_name, 'NewFirstName')  # Check if the update worked
        self.assertEqual(self.user_student.last_name, 'NewLastName')  # Check if the update worked
        self.assertEqual(self.user_student.email, 'newemail@example.com')  # Check if the update worked

    def test_profile_update_invalid_data(self):
        self.client.login(username='teacher_user', password='password123')
        response = self.client.post(reverse('profile'), {
            'first_name': '',
            'last_name': '',
            'email': 'invalidemail',  # Invalid email format
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the profile page
       

    def test_profile_update_message_success(self):
        self.client.login(username='teacher_user', password='password123')
        response = self.client.post(reverse('profile'), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'username':'teacher_user',
            'user_type':'teacher',
            'password':'password123',
            'is_staff':True,             
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]
       
