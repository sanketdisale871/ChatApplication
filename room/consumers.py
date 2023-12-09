import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message,Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the room name from the URL parameters
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        # Create a unique group name for the room
        self.room_group_name = 'chat_%s' % self.room_name

        # Add the WebSocket connection to the group associated with the room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self):
        # Remove the WebSocket connection from the group associated with the room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # When a message is received from the WebSocket
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        # Send the message to the group (all clients in the same chat room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room
            }
        )

    async def chat_message(self, event):
        # When a message is sent to the group
        message = event['message']
        username = event['username']
        room = event['room']

        await self.save_message(username,room,message)

        # Send the message back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room  # Corrected the duplicated 'username' key to 'room'
        }))


    @sync_to_async
    def save_message(self,username,room,message):
        user = User.objects.get(username=username)
        room=Room.objects.get(slug=room)

        Message.objects.create(user=user,room=room,content=message)



    


