"""
Wallet Serializers
"""

from rest_framework import serializers
from .models import Wallet, WalletTransaction


class WalletSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "user", "user_name", "balance", "is_active", "last_updated", "created_at"]
        read_only_fields = ["balance", "last_updated"]


class WalletTransactionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)

    class Meta:
        model = WalletTransaction
        fields = ["id", "amount", "transaction_type", "type_display", "description", "created_at"]
