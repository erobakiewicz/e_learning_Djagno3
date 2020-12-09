import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer to connect, disconnect and receive messages text as jsons
    by the key and then echo it via self.send().
    ChatConsumer is using asyncwebsocket for asynchronous calls
    async def + await: for async functioning
    """

    async def connect(self):
        """
        async_to_sync(): wraps calls  to asynchronous channel layer
        Retrieve id of course for chat, build chat for course and name it,
        provide "add to chat" functionality, keep the call by self.accept() with
        WebSocket connection.
        :return:
        """
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat()
            }
        )

    # retrieve message from room group
    async def chat_message(self, event):
        # send message to WebSocket, match "type" key with group
        await self.send(text_data=json.dumps(event))