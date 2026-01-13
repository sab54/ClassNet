from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm, CustomPasswordChangeForm, UserSearchForm, UserUpdateForm
from django.core.exceptions import ValidationError


class UserRegistrationFormTestCase(TestCase):
    
    def test_user_registration_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student',
            'profile_picture': None,  # Assuming you're not testing file uploads here
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student',
            'profile_picture': None,
            'password': 'password123',
            'confirm_password': 'wrongpassword123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', form.errors['__all__'])

    def test_user_registration_form_missing_field(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student',
            'profile_picture': None,
            'password': 'password123',
            # Missing confirm_password field
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['confirm_password'])


class CustomPasswordChangeFormTestCase(TestCase):

    def test_password_change_form_valid_data(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            user_type='student'
        )
        form_data = {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        form = CustomPasswordChangeForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_change_form_password_mismatch(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            user_type='student'
        )
        form_data = {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'wrongnewpassword123',
        }
        form = CustomPasswordChangeForm(user=user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('The two password fields didn’t match.', form.errors['new_password2'])


class UserSearchFormTestCase(TestCase):

    def test_user_search_form_valid_data(self):
        form_data = {'query': 'testuser'}
        form = UserSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_search_form_invalid_data(self):
        form_data = {'query': 'ab'}  # Query too short, less than 3 characters
        form = UserSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at least 3 characters (it has 2).', form.errors['query'])

    def test_user_search_form_no_query(self):
        form_data = {'query': ''}
        form = UserSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # It's valid since 'query' is optional


class UserUpdateFormTestCase(TestCase):

    def test_user_update_form_valid_data(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            user_type='student'
        )
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'profile_picture': None,  # Assuming no file upload for the test
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_user_update_form_missing_field(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            user_type='student'
        )
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            # Missing last_name
            'profile_picture': None,
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['last_name'])
