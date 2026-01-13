from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model to represent messages within a room.

    This serializer is used to serialize and deserialize message data. It includes the content
    of the message, the user who sent it, and the timestamp when it was sent.
    """
    class Meta:
        model = Message
        fields = ['id', 'room_name', 'message', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
