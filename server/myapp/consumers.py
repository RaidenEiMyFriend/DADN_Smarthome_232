# consumers.py

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("data_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("data_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send("data_group", {
            "type": "data.message",
            "message": message,
        })

    async def data_message(self, event):
        message = event['message']
        text_data = json.dumps({
            'message': message
        })
        print("Message that send to Websocket:  ", text_data)
        
        await self.send(text_data)
