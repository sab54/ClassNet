from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Custom Manager for the User Model
class CustomUserManager(BaseUserManager):
    """
    Custom manager for creating users and superusers with additional functionality.
    """
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a regular user with a username, email, and password.
        """
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password before storing it
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with a username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that extends Django's AbstractBaseUser and PermissionsMixin.
    The model includes core fields like username, first name, email, profile picture,
    user type, and additional functionality for managing users and permissions.
    """
    STUDENT = 'student'
    TEACHER = 'teacher'
    
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    # Core User fields
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Additional fields for users
    bio = models.TextField(null=True, blank=True)  # Short biography of the user

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    # Permissions for teachers to access students' records
    def can_view_student_data(self, user):
        return self.user_type == self.TEACHER and user.user_type == self.STUDENT

    class Meta:
        permissions = [
            ("can_view_student_data", "Can view student data")
        ]
