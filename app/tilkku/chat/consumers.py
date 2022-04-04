import json
from datetime import datetime

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.room = await sync_to_async(Room.objects.get)(name=self.room_name)
        self.user = self.scope['user']

        # Join room group
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            now = datetime.now()
            timestamp = now.strftime("%H:%M")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.first_name + ' ' + self.user.last_name,
                    'time': timestamp
                }
            )
            await sync_to_async(self.room.online.add)(self.user)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.user.is_authenticated:
            now = datetime.now()
            timestamp = now.strftime("%H:%M")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.first_name + ' ' + self.user.last_name,
                    'time': timestamp
                }
            )
            await sync_to_async(self.room.online.remove)(self.user)

    async def receive(self, text_data=None, blob_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #sender = text_data_json['sender']
        #user = text_data_json['user']

        if not self.user.is_authenticated:
            return

        now = datetime.now()
        timestamp = now.strftime("%H:%M")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.first_name + ' ' + self.user.last_name,
                'user': self.user.username,
                'time': timestamp
            }
        )

        await sync_to_async(Message.objects.create)(user=self.user, room=self.room, content=message)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        user = event['user']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'user': user,
            'time': time
        }))
