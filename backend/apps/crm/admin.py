"""
CRM Admin
"""

from django.contrib import admin
from .models import CustomerInteraction, BulkSMS


@admin.register(CustomerInteraction)
class CustomerInteractionAdmin(admin.ModelAdmin):
    list_display = ["customer", "interaction_type", "description", "created_at"]
    list_filter = ["interaction_type", "created_at"]
    search_fields = ["customer__phone", "description"]


@admin.register(BulkSMS)
class BulkSMSAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "sent_count", "created_at"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["sent_count", "created_at"]
