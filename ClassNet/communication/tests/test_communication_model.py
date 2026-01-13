from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from communication.models import StatusUpdate
from datetime import datetime
from django.utils import timezone

class StatusUpdateModelTestCase(TestCase):

    def setUp(self):
        # Create a student user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password',
            user_type='student',
            is_staff=False,
        )

        # Create a non-student user (e.g., a teacher)
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,  # Ensure the user is a staff
        )

    def test_status_update_creation(self):
        """
        Test that a StatusUpdate object can be created with valid data.
        """
        # Create a status update
        status_update = StatusUpdate.objects.create(
            user=self.user,
            content="This is a status update!"
        )

        # Check if the status update was created successfully
        self.assertEqual(status_update.user, self.user)
        self.assertEqual(status_update.content, "This is a status update!")
        self.assertTrue(isinstance(status_update.timestamp, datetime))  # Ensure timestamp is a datetime object

    def test_str_method(self):
        """
        Test the string representation of the StatusUpdate model.
        """
        status_update = StatusUpdate.objects.create(
            user=self.user,
            content="Another status update."
        )

        # Format the expected string
        expected_str = f"{self.user.username} - {status_update.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Check if the __str__ method returns the correct string
        self.assertEqual(str(status_update), expected_str)

    def test_status_update_ordering(self):
        """
        Test that status updates are ordered by timestamp in descending order.
        """
        # Create two status updates with different timestamps
        status_update1 = StatusUpdate.objects.create(
            user=self.user,
            content="First status update"
        )
        status_update2 = StatusUpdate.objects.create(
            user=self.user,
            content="Second status update"
        )

        # Get the status updates ordered by timestamp
        status_updates = StatusUpdate.objects.all()

        # Check if the status updates are ordered by the latest first
        self.assertEqual(status_updates[0], status_update2)
        self.assertEqual(status_updates[1], status_update1)

    def test_timestamp_auto_now_add(self):
        """
        Test that the timestamp field is automatically set.
        """
        # Create a status update
        status_update = StatusUpdate.objects.create(
            user=self.user,
            content="Check the timestamp"
        )

        # Ensure the timestamp is set to the current time
        self.assertTrue(status_update.timestamp <= timezone.now())  # The timestamp should be the current time or earlier
