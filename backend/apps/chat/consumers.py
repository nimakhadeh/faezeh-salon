"""
Chat WebSocket Consumer
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # Check if user is part of this room
        is_member = await self.is_room_member(self.room_id, self.user.id)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        msg_type = data.get("type", "text")

        # Save message to database
        msg = await self.save_message(self.room_id, self.user.id, message, msg_type)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "msg_type": msg_type,
                "sender_id": self.user.id,
                "sender_name": self.user.full_name,
                "message_id": msg.id,
                "timestamp": str(msg.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "type": event["msg_type"],
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
            "message_id": event["message_id"],
            "timestamp": event["timestamp"],
        }))

    @database_sync_to_async
    def is_room_member(self, room_id, user_id):
        from .models import ChatRoom
        try:
            room = ChatRoom.objects.get(id=room_id)
            return room.customer_id == user_id or room.specialist_id == user_id
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, room_id, user_id, content, msg_type):
        from .models import ChatRoom, ChatMessage
        room = ChatRoom.objects.get(id=room_id)
        return ChatMessage.objects.create(
            room=room,
            sender_id=user_id,
            content=content,
            message_type=msg_type,
        )
