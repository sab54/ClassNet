# serializers.py
from rest_framework import serializers
from .models import StatusUpdate

class StatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the StatusUpdate model.

    This serializer is responsible for converting the `StatusUpdate` model instances
    into a format that can be easily rendered into JSON, XML, or other content types.
    It also validates incoming data when creating or updating a status update.

    Fields:
        id (IntegerField): The unique identifier of the status update.
        user (PrimaryKeyRelatedField): The user who created the status update.
        content (CharField): The content of the status update message.
        timestamp (DateTimeField): The timestamp when the status update was created.

    Meta:
        model (StatusUpdate): Specifies that this serializer works with the `StatusUpdate` model.
        fields (list): Specifies which fields from the model to include in the serialized output.
    """
    class Meta:
        model = StatusUpdate
        fields = ['id', 'user', 'content', 'timestamp']  # Fields to be included in the serialized data
