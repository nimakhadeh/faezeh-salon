"""
Wallet Admin
"""

from django.contrib import admin
from .models import Wallet, WalletTransaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "is_active", "last_updated"]
    search_fields = ["user__phone", "user__first_name"]


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet", "amount", "transaction_type", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["wallet__user__phone"]
