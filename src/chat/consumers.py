import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Thread
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.admin = await self.get_admin('tilek')
        self.user = self.scope['user']
        self.thread = await self.get_thread(self.admin, self.scope['user'])
        await self.accept()
        if self.thread == None:
            now = timezone.now()
            await self.send(text_data=json.dumps({
                'message': 'Please log in to send message',
                'user': 'Shop',
                'datetime': now.isoformat()}))
            return
        self.room_group_name = f'chat_{self.thread.id}'
        self.thread.name = self.room_group_name
        await self.save_thread()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Leave room group
        # await self.delete_thread(self.thread)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat()
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_thread(self, admin, user):
        return Thread.objects.get_or_create_personal_thread(admin, user)

    @database_sync_to_async
    def get_admin(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def delete_thread(self, thread):
        Thread.objects.filter(id=thread.id).delete()

    @database_sync_to_async
    def get_first_thread(self):
        return Thread.objects.get_by_user(self.admin)

    @database_sync_to_async
    def save_thread(self):
        self.thread.save()
        