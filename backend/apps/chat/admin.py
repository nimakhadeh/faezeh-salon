"""
Chat Admin
"""

from django.contrib import admin
from .models import ChatRoom, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ["created_at"]


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["customer", "specialist", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["customer__phone", "specialist__phone"]
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["room", "sender", "content_preview", "is_read", "created_at"]
    list_filter = ["is_read", "message_type", "created_at"]
    search_fields = ["content", "sender__phone"]

    @admin.display(description="محتوا")
    def content_preview(self, obj):
        return obj.content[:50]
