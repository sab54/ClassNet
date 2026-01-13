from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class ChatViewsTestCase(TestCase):
    def setUp(self):
        # Create a student user
        self.student_user = get_user_model().objects.create_user(
            username='test_user',
            first_name='Tester',
            last_name='User',
            email='user@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

    def test_index_view(self):
        """Test the index view."""
        # Log in as a student user
        self.client.login(username='test_user', password='password123')

        # Perform the GET request
        response = self.client.get(reverse('index'))
        
        # Check if the response is 200 OK and contains the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/index.html')

    def test_room_view(self):
        """Test the room view with a room name."""
        # Log in as a student user
        self.client.login(username='test_user', password='password123')
        room_name = 'testroom'

        # Perform the GET request to the room view
        response = self.client.get(reverse('room', kwargs={'room_name': room_name}))
        
        # Check if the response is 200 OK and contains the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        
        # Check if the room_name context variable is passed correctly
        self.assertContains(response, f'Room: {room_name}')