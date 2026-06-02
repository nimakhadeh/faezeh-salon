"""
Chat Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class MyChatRoomsView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return ChatRoom.objects.all()
        elif user.role == "specialist":
            return ChatRoom.objects.filter(specialist=user)
        return ChatRoom.objects.filter(customer=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return ChatRoom.objects.all()
        elif user.role == "specialist":
            return ChatRoom.objects.filter(specialist=user)
        return ChatRoom.objects.filter(customer=user)


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        room = get_object_or_404(ChatRoom, id=room_id)
        user = self.request.user

        if user.role == "admin" or room.customer == user or room.specialist == user:
            return ChatMessage.objects.filter(room=room)
        return ChatMessage.objects.none()


class CreateChatRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        specialist_id = request.data.get("specialist")
        appointment_id = request.data.get("appointment")

        if not specialist_id:
            return Response({"error": "specialist is required."}, status=400)

        from apps.accounts.models import User
        try:
            specialist = User.objects.get(id=specialist_id, role="specialist")
        except User.DoesNotExist:
            return Response({"error": "Specialist not found."}, status=404)

        # Check if room already exists
        room, created = ChatRoom.objects.get_or_create(
            customer=request.user,
            specialist=specialist,
            defaults={"appointment_id": appointment_id},
        )

        if appointment_id and not room.appointment_id:
            room.appointment_id = appointment_id
            room.save()

        return Response({
            "room": ChatRoomSerializer(room, context={"request": request}).data,
            "created": created,
        })


class MarkMessagesReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if room.customer == request.user or room.specialist == request.user:
            room.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
            return Response({"message": "Messages marked as read."})
        return Response({"error": "Access denied."}, status=403)
