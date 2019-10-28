import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class ViewConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        self.trigger()

        # self.scope['user']

    async def trigger(self):
        await self.send({
            "type": "websocket.send",
        })

    async def websocket_receive(self, event):
        print("Received", event)

    async def websocket_disconnect(self, event):
        print("Disconnected", event)