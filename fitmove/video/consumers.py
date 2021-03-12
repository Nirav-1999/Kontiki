import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive BlazePose co-ordinates
    def receive(self, text_data):
        # print(self.channel_name)
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['points']
        except:
            message = ''
        # print(message)
        # other_channel = k if k not in
        # print(self.room_group_name)
        other_channel = ''
        for k in list(self.channel_layer.group_channels[self.room_group_name].keys()):
            # name = k.split('!')[-1]
            # print("================")
            # print(name)
            if k != self.channel_name:
                # print("Now Break")
                other_channel = k
                break
        # print("Chnnel")
        # print(self.channel_name)
        # print(other_channel)
        # for k in self.channel_layer.groups['chat_lobby'].keys:
        #     print(k)
        # print(list(self.channel_layer.groups['chat_lobby'].keys()))


        # Send message to second channel
        if other_channel != '':
            async_to_sync(self.channel_layer.send)(
                other_channel,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    # Receive message from second channel
    def chat_message(self, event):
        # print(self.channel_name)

        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
