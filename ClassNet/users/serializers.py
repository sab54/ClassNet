from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model to control how user data is serialized.
    This serializer defines which fields to include when returning user data, 
    as well as how to validate incoming data for creating or updating users.
    """
    # You may want to exclude the password field from the response
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'user_type', 'bio', 'is_active', 'is_staff', 'date_joined', 'password']
        read_only_fields = ['id', 'date_joined']  # Don't allow updating 'id' and 'date_joined'

    def create(self, validated_data):
        """
        Overriding the create method to hash the password when creating the user
        """
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle password changes.
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
