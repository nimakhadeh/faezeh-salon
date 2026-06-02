"""
Payments Admin
"""

from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user", "amount", "transaction_type",
        "status", "authority", "ref_id", "created_at",
    ]
    list_filter = ["status", "transaction_type", "created_at"]
    search_fields = ["user__phone", "authority", "ref_id"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
