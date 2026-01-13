from django.shortcuts import render
from .models import Message
from rest_framework import generics
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    """
    API view to create a new message in a specific room.
    
    This view allows users to send messages in a specific chat room.
    The user must provide the message content, and the room ID is used to determine
    where the message should be sent.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save()

# Create your views here.
def index(request):
    """
    Handles GET requests to retrieve the details of a specific room.    
    Renders index.html with room names
    """
    # Fetch all distinct room names from the Message model
    room_names = Message.objects.values_list('room_name', flat=True).distinct()
    return render(request, 'chat/index.html', {'room_names': room_names})

def room(request, room_name):
    """
    Handles GET requests to retrieve the details of a specific room.
    
    This method retrieves a room by its ID and returns its data along with
    a list of messages sent in that room.
    """
    return render(request, 'chat/room.html', {'room_name': room_name })


