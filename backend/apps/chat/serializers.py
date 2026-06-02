"""
Chat Serializers
"""

from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    sender_avatar = serializers.ImageField(source="sender.avatar", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id", "room", "sender", "sender_name", "sender_avatar",
            "content", "message_type", "file_url", "is_read", "created_at",
        ]
        read_only_fields = ["sender", "is_read"]


class ChatRoomSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    specialist_name = serializers.CharField(source="specialist.full_name", read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id", "customer", "customer_name", "specialist", "specialist_name",
            "appointment", "is_active", "created_at", "updated_at",
            "last_message", "unread_count",
        ]

    def get_last_message(self, obj):
        msg = obj.last_message
        if msg:
            return {
                "content": msg.content[:100],
                "sender": msg.sender.full_name,
                "created_at": msg.created_at,
            }
        return None

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if request:
            return obj.messages.exclude(sender=request.user).filter(is_read=False).count()
        return 0
