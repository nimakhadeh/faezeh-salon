"""
Chat URLs
"""

from django.urls import path
from .views import (
    MyChatRoomsView, ChatRoomDetailView,
    ChatMessageListView, CreateChatRoomView,
    MarkMessagesReadView,
)

urlpatterns = [
    path("rooms/", MyChatRoomsView.as_view(), name="chat_rooms"),
    path("rooms/create/", CreateChatRoomView.as_view(), name="create_room"),
    path("rooms/<int:pk>/", ChatRoomDetailView.as_view(), name="room_detail"),
    path("rooms/<int:room_id>/messages/", ChatMessageListView.as_view(), name="room_messages"),
    path("rooms/<int:room_id>/read/", MarkMessagesReadView.as_view(), name="mark_read"),
]
