from django.conf import settings
from django.db import models

class Message(models.Model):
    """
    Represents a single message in a chat room.

    Each message belongs to a specific Room and is sent by a specific User.
    Messages can be text-based or media-based (depending on how you expand the model).
    """
    room_name = models.CharField(max_length=255)
    message = models.TextField()
    # ForeignKey to the User model. It uses `settings.AUTH_USER_MODEL` to refer to the user model dynamically.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.created_at}] {self.message[:50]}... in room {self.room_name}'
