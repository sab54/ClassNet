from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class CustomUserTestCase(TestCase):
    
    def test_create_user(self):
        # Create a regular user
        user = get_user_model().objects.create_user(
            username="testuser", 
            email="testuser@example.com", 
            password="password123",
            first_name="Test", 
            last_name="User",
            user_type="student"
        )
        
        # Check that the user was created successfully
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.user_type, "student")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        # Create a superuser
        superuser = get_user_model().objects.create_superuser(
            username="admin", 
            email="admin@example.com", 
            password="admin123"
        )

        # Check that the superuser is created correctly
        self.assertEqual(superuser.username, "admin")
        self.assertTrue(superuser.check_password("admin123"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_create_user_without_username(self):
        # Ensure creating a user without a username raises an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username="", 
                email="testuser@example.com", 
                password="password123"
            )
    
    def test_get_full_name(self):
        user = get_user_model().objects.create_user(
            username="testuser", 
            email="testuser@example.com", 
            password="password123", 
            first_name="Test", 
            last_name="User",
            user_type="student"
        )

        # Test the `get_full_name` method
        self.assertEqual(user.get_full_name(), "Test User")
    
    def test_get_short_name(self):
        user = get_user_model().objects.create_user(
            username="testuser", 
            email="testuser@example.com", 
            password="password123", 
            first_name="Test", 
            last_name="User",
            user_type="student"
        )

        # Test the `get_short_name` method
        self.assertEqual(user.get_short_name(), "Test")

    def test_can_view_student_data(self):
        # Create a teacher and a student
        teacher = get_user_model().objects.create_user(
            username="teacher1", 
            email="teacher1@example.com", 
            password="password123", 
            first_name="Teacher", 
            last_name="One",
            user_type="teacher"
        )

        student = get_user_model().objects.create_user(
            username="student1", 
            email="student1@example.com", 
            password="password123", 
            first_name="Student", 
            last_name="One",
            user_type="student"
        )

        # Teacher should have permission to view student data
        self.assertTrue(teacher.can_view_student_data(student))
    
    def test_can_view_student_data_for_non_teacher(self):
        # Create a user who is not a teacher
        user = get_user_model().objects.create_user(
            username="user1", 
            email="user1@example.com", 
            password="password123", 
            first_name="User", 
            last_name="One",
            user_type="student"
        )

        # Non-teachers should not have permission to view student data
        student = get_user_model().objects.create_user(
            username="student2", 
            email="student2@example.com", 
            password="password123", 
            first_name="Student", 
            last_name="Two",
            user_type="student"
        )

        self.assertFalse(user.can_view_student_data(student))

    def test_email_unique(self):
        # Ensure that email is unique
        get_user_model().objects.create_user(
            username="user1", 
            email="testuser@example.com", 
            password="password123", 
            first_name="User", 
            last_name="One", 
            user_type="student"
        )
        
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="user2", 
                email="testuser@example.com", 
                password="password123", 
                first_name="User", 
                last_name="Two", 
                user_type="teacher"
            )
