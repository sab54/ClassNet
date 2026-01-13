from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.models import Message
from datetime import datetime
from django.utils import timezone

CustomUser = get_user_model()

class MessageConsumersTest(TestCase):

    def setUp(self):
        """
        Set up the necessary data for testing.
        """
                # Create a student user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Tester',
            last_name='User',
            email='user@example.com',
            password='password',
            user_type='student',
            is_staff=False,
        )

        self.room_name = 'TestRoom'
        self.message_content = 'This is a test message.'
        self.message = Message.objects.create(
            room_name=self.room_name,
            message=self.message_content,
            user=self.user
        )
    
    def test_message_creation(self):
        """
        Test that a message is created successfully.
        """
        self.assertEqual(self.message.room_name, self.room_name)
        self.assertEqual(self.message.message, self.message_content)
        self.assertEqual(self.message.user.username, 'testuser')
        self.assertTrue(isinstance(self.message.created_at, datetime))  # Ensure created_at is set

    def test_message_str(self):
        """
        Test the string representation of a message.
        """
        truncated_message = self.message_content[:50] + '.' if len(self.message_content) > 50 else self.message_content
        expected_str = f'[{self.message.created_at}] {truncated_message}... in room {self.room_name}'
        self.assertEqual(str(self.message), expected_str)

    def test_message_created_at(self):
        """
        Test that the `created_at` timestamp is automatically set upon creation.
        """
        now = timezone.now()
        self.assertTrue(self.message.created_at <= now)

    def test_message_empty_message_field(self):
        """
        Test that a message can be created with an empty `message` field.
        """
        empty_message = Message.objects.create(
            room_name=self.room_name,
            message='',
            user=self.user
        )
        self.assertEqual(empty_message.message, '')

    def test_message_empty_room_name_field(self):
        """
        Test that a message can be created with an empty `room_name` field.
        """
        empty_room_name = Message.objects.create(
            room_name='',
            message=self.message_content,
            user=self.user
        )
        self.assertEqual(empty_room_name.room_name, '')

    def test_message_user_deletion(self):
        """
        Test that when the associated user is deleted, their messages are also deleted (Cascade behavior).
        """
        user_to_delete = CustomUser.objects.create_user(username='deleteuser', password='password')
        message_to_delete = Message.objects.create(
            room_name='DeleteRoom',
            message='This is a message that should be deleted with the user.',
            user=user_to_delete
        )
        user_to_delete.delete()

        # Check that the message is deleted when the user is deleted
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message_to_delete.id)

    def test_message_creation_with_long_message(self):
        """
        Test that a message longer than 50 characters is handled correctly.
        """
        long_message = 'This is a long message designed to test the truncation behavior in the string representation of the message model.'
        message = Message.objects.create(
            room_name=self.room_name,
            message=long_message,
            user=self.user
        )

        self.assertEqual(message.message, long_message)  # Ensure the message is stored correctly
        # Ensure the string representation is truncated to 50 characters
        self.assertTrue(str(message).endswith('... in room TestRoom'))

    def test_message_creation_with_special_characters(self):
        """
        Test that messages with special characters are handled correctly.
        """
        special_message = 'This is a special message with special characters like !@#$%^&*()'
        message = Message.objects.create(
            room_name=self.room_name,
            message=special_message,
            user=self.user
        )
        self.assertEqual(message.message, special_message)


    def test_message_without_room_name(self):
        """
        Test that a message can be created without a room name.
        """
        message_without_room = Message.objects.create(
            room_name='',
            message=self.message_content,
            user=self.user
        )
        self.assertEqual(message_without_room.room_name, '')  # Room name can be empty

    def test_message_max_length_room_name(self):
        """
        Test that the room name is correctly limited to 255 characters.
        """
        long_room_name = 'A' * 256  # 256 characters
        message = Message.objects.create(
            room_name=long_room_name[:255],  # Truncate to 255 characters
            message=self.message_content,
            user=self.user
        )
        self.assertEqual(message.room_name, long_room_name[:255])
