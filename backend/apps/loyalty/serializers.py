"""
Loyalty Serializers
"""

from rest_framework import serializers
from .models import LoyaltyRule, LoyaltyPoint, LoyaltyTransaction


class LoyaltyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyRule
        fields = [
            "id", "name", "points_per_amount", "amount_threshold",
            "points_to_discount", "discount_amount", "is_active",
        ]


class LoyaltyPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoint
        fields = ["points", "total_earned", "total_spent", "updated_at"]


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)

    class Meta:
        model = LoyaltyTransaction
        fields = ["id", "points", "transaction_type", "type_display", "description", "created_at"]


class ConvertPointsSerializer(serializers.Serializer):
    points = serializers.IntegerField(min_value=1, required=True)
