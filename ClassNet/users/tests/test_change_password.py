from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth import update_session_auth_hash

class ChangePasswordTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='password123',  # Initial password
            user_type='teacher',
            is_staff=True
        )

    def test_change_password_logged_in_user(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Send a valid password change request
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })

        # Ensure the password was changed and the user is redirected
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password change
        self.assertRedirects(response, reverse('profile'))  # Should redirect to the profile page

        # Check if success message is present
        messages = [m.message for m in get_messages(response.wsgi_request)]

    def test_change_password_invalid_current_password(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Attempt to change the password with an invalid old password
        response = self.client.post(reverse('change_password'), {
            'old_password': 'wrongpassword',  # Invalid old password
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })

        # Ensure the form is not valid, and the user is not redirected
        self.assertEqual(response.status_code, 200)  # Should remain on the password change page
        self.assertContains(response, "Please correct the error below.")  # Error message shown

        # Ensure the password remains the same
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('password123'))

    def test_change_password_non_matching_new_passwords(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Attempt to change the password with non-matching new passwords
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword456',  # Non-matching passwords
        })

        # Ensure the form is not valid, and the user is not redirected
        self.assertEqual(response.status_code, 200)  # Should remain on the password change page
        self.assertContains(response, "Please correct the error below.")  # Error message shown

        # Ensure the password remains the same
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('password123'))

    def test_change_password_weak_new_password(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Attempt to change the password with a weak new password (e.g., too short)
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password123',
            'new_password1': 'short',  # Invalid short password
            'new_password2': 'short',  # Invalid short password
        })

        # Ensure the form is not valid, and the user is not redirected
        self.assertEqual(response.status_code, 200)  # Should remain on the password change page
        self.assertContains(response, "Please correct the error below.")  # Error message shown

        # Ensure the password remains the same
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('password123'))

    def test_change_password_redirect_for_unauthenticated_user(self):
        # Ensure unauthenticated users are redirected to the login page
        response = self.client.get(reverse('change_password'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('change_password'))

    def test_change_password_session_update(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Send a valid password change request
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })

        # Check if session is updated after password change to avoid logout
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'testuser')
