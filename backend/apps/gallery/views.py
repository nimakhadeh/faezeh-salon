"""
Gallery Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone

from .models import GalleryImage
from .serializers import (
    GalleryImageSerializer, GalleryImageUploadSerializer,
    GalleryImageApproveSerializer,
)


class PublicGalleryListView(generics.ListAPIView):
    """Public gallery - only approved images"""
    queryset = GalleryImage.objects.filter(status="approved", is_public=True)
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.AllowAny]


class MyGalleryListView(generics.ListAPIView):
    """Customer's own uploads"""
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GalleryImage.objects.filter(customer=self.request.user)


class GalleryUploadView(generics.CreateAPIView):
    serializer_class = GalleryImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return GalleryImage.objects.all()
        return GalleryImage.objects.filter(customer=user)


class GalleryPendingListView(generics.ListAPIView):
    """Admin: list pending images for approval"""
    queryset = GalleryImage.objects.filter(status="pending")
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class GalleryApproveView(generics.UpdateAPIView):
    """Admin: approve/reject gallery images"""
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageApproveSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(reviewed_at=timezone.now())


class SpecialistGalleryView(generics.ListAPIView):
    """List gallery images for a specific specialist"""
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        specialist_id = self.kwargs.get("specialist_id")
        return GalleryImage.objects.filter(
            specialist_id=specialist_id,
            status="approved",
            is_public=True,
        )
