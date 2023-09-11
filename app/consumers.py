from channels.generic.websocket import AsyncWebsocketConsumer
import json
from app.models import Chat, User
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async

class TokenAuthenticationError(Exception):
    pass

@database_sync_to_async
def get_chat_room(room_name):
    try:
        return Chat.objects.get(name=room_name)
    except Chat.DoesNotExist:
        return None
    
@database_sync_to_async
def check_user_in_chat(chat_room, user_id):
    return chat_room.participants.filter(id=user_id).exists()

@database_sync_to_async
def is_user_online(current_user, participants):
    online_participants = []
    for participant in participants:
            if participant.id != current_user.id and participant.is_online:
                online_participants.append(participant.name)
    return len(online_participants)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        current_user = self.scope.get('user')
        if current_user is None:
           raise TokenAuthenticationError("Authentication failed")
            
        chat_room = await get_chat_room(self.room_name)    

        if chat_room is None:
           raise TokenAuthenticationError("Chat not found")
        
        user_in_chat = await check_user_in_chat(chat_room, current_user.id)

        if not user_in_chat:
           raise TokenAuthenticationError("You are not in the chat")
        
        participants = chat_room.participants.all()

        user_online = await is_user_online(current_user, participants)
        if not user_online:
            raise TokenAuthenticationError("user is Offline")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class SendMessageConsumer(ChatConsumer):
    async def connect(self):
        await super().connect()

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive(self, text_data):
        await super().receive(text_data)