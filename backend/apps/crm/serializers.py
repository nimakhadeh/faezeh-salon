"""
CRM Serializers
"""

from rest_framework import serializers
from .models import CustomerInteraction, BulkSMS


class CustomerInteractionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    type_display = serializers.CharField(source="get_interaction_type_display", read_only=True)

    class Meta:
        model = CustomerInteraction
        fields = [
            "id", "customer", "customer_name", "interaction_type",
            "type_display", "description", "reference_id", "created_at",
        ]


class BulkSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkSMS
        fields = ["id", "title", "message", "recipients", "filter_criteria", "status", "sent_count", "created_at"]
        read_only_fields = ["status", "sent_count"]


class CustomerSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    phone = serializers.CharField()
    total_appointments = serializers.IntegerField()
    total_spent = serializers.IntegerField()
    last_visit = serializers.DateTimeField()
    avg_nps = serializers.FloatField()
    loyalty_points = serializers.IntegerField()
