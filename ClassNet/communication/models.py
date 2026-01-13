from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class StatusUpdate(models.Model):
    """
    Model to represent a status update by a user.

    This model stores a status update made by a user. Each status update
    is associated with a specific user, has a content field to store the
    status message, and a timestamp to track when the update was created.

    Fields:
        user (ForeignKey): The user who posted the status update.
        content (TextField): The content or message of the status update.
        timestamp (DateTimeField): The date and time when the status update was created, automatically set to the time of creation.

    Meta:
        ordering (list): The status updates are ordered by timestamp in descending order, 
                          so the most recent update appears first.

    Methods:
        __str__(): Returns a human-readable string representation of the status update
                   containing the username of the user and the formatted timestamp.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='status_updates')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ['-timestamp']  # Order the updates by the most recent first
