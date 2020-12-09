import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """
    Consumer to connect, disconnect and receive messages text as jsons
    by the key and then echo it via self.send().
    """

    def connect(self):
        """
        async_to_sync(): wraps calls  to asynchronous channel layer
        Retrieve id of course for chat, build chat for course and name it,
        provide "add to chat" functionality, keep the call by self.accept() with
        WebSocket connection.
        :return:
        """
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # retrieve message from room group
    def chat_message(self, event):
        # send message to WebSocket, match "type" key with group
        self.send(text_data=json.dumps(event))