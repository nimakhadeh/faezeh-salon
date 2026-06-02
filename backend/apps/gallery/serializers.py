"""
Gallery Serializers
"""

from rest_framework import serializers
from .models import GalleryImage
from apps.accounts.serializers import UserSerializer


class GalleryImageSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    specialist_name = serializers.CharField(source="specialist.full_name", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = GalleryImage
        fields = [
            "id", "customer", "customer_name",
            "specialist", "specialist_name",
            "image_before", "image_after",
            "service", "service_name",
            "description", "status", "status_display",
            "is_public", "uploaded_at", "reviewed_at", "review_note",
        ]
        read_only_fields = ["status", "reviewed_at", "review_note"]


class GalleryImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["specialist", "service", "image_before", "image_after", "description"]


class GalleryImageApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["status", "is_public", "review_note"]
