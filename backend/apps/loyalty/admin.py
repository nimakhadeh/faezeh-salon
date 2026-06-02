"""
Loyalty Admin
"""

from django.contrib import admin
from .models import LoyaltyRule, LoyaltyPoint, LoyaltyTransaction


@admin.register(LoyaltyRule)
class LoyaltyRuleAdmin(admin.ModelAdmin):
    list_display = ["name", "points_per_amount", "amount_threshold", "points_to_discount", "discount_amount", "is_active"]
    list_editable = ["is_active"]


@admin.register(LoyaltyPoint)
class LoyaltyPointAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "total_earned", "total_spent"]
    search_fields = ["user__phone", "user__first_name"]


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "transaction_type", "created_at"]
    list_filter = ["transaction_type", "created_at"]
