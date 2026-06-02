"""
Payments Serializers
"""

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "user", "user_name", "amount", "transaction_type",
            "type_display", "status", "status_display", "authority",
            "ref_id", "reference_id", "description", "metadata",
            "card_pan", "created_at", "updated_at",
        ]
        read_only_fields = [
            "status", "authority", "ref_id", "card_pan",
            "created_at", "updated_at",
        ]


class PaymentRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1000)
    transaction_type = serializers.ChoiceField(choices=Transaction.TYPE_CHOICES)
    description = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.JSONField(required=False, default=dict)


class PaymentVerifySerializer(serializers.Serializer):
    authority = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
