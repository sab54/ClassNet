import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message  # Make sure you import the Message model
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer that handles real-time chat communication between users.
    This consumer allows clients to connect, send messages to a specific room,
    and receive messages broadcasted to all connected users in that room.

    The flow:
    1. The user connects to the WebSocket, specifying a room to join.
    2. The consumer joins the specified room group.
    3. When a message is received from the WebSocket, it is broadcast to all members of the room group.
    4. When a message is sent to the room group, the consumer sends it to all connected clients in the room.
    """

    async def connect(self):  
        """
        Called when the WebSocket is handshaking as part of the connection process.

        - Retrieves the room name from the URL parameters.
        - Constructs a unique group name for the chat room.
        - Adds the consumer to the room group (channel layer group).
        - Accepts the WebSocket connection, allowing the client to communicate.
        """
        await self.accept()  

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Get the last 10 messages asynchronously
        messages = await self.get_message_history(self.room_name)

        # Send message history to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages,
        }))


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


    @database_sync_to_async
    def get_message_history(self, room_name):
        # Query the last 10 messages from the database
        messages = Message.objects.filter(room_name=room_name).order_by('-created_at')[:10]
        result =[]
        for msg in messages:
            # Create a dictionary with message and created_at values
            msg_dict = {
                "message": msg.message,
                "created_at":  msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "username": msg.user.username,
            }
            # Append the dictionary to the result list
            result.append(msg_dict)
        return result

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.

        - Removes the consumer from the room group, ensuring no further messages are sent to this client.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
         )

    # Receive message from WebSocket
    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.

        - Decodes the incoming message and extracts the content.
        - Sends the message to the room group, so it can be broadcast to all other connected clients in the same room.
        """

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message.strip():  # Check if the message is not empty (ignoring spaces)
            user = self.scope['user']
            # Save message to the database
            data = await self.save_message(self.room_name, message, user)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data,
                }
            )
        else:
            # Optionally, handle empty messages (e.g., logging, sending a warning)
            pass
    
    @database_sync_to_async
    def save_message(self, room_name, message, user):
        try:
            # Ensure the user exists or get the user from the provided username
            if user:
                return Message.objects.create(room_name=room_name, message=message, user=user)
            else:
                print("Error: User is required to save the message.")
        except Exception as e:
            # Log or handle any errors that occur during message saving
            print(f"Error saving message: {e}")
            # Optionally, you could log to the database or handle the error in a different way


    # Receive message from room group
    async def chat_message(self, event):
        """
        Called when a message is received from the room group.

        - This is where the server sends messages to the WebSocket connection.
        - It is triggered when a message is broadcast to the room group.
        - The message is sent back to the client that originally made the WebSocket connection.
        """
        data = event['message']
        message = data.message
        date = data.created_at.isoformat()
        username = data.user.username
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'date': date,
            'username' : username,
        }))


