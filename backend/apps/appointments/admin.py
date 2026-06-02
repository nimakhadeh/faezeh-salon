"""
Appointments Admin
"""

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "id", "customer", "specialist", "service", "date",
        "start_time", "status", "deposit_amount", "final_price",
        "created_at",
    ]
    list_filter = ["status", "date", "specialist", "service"]
    search_fields = ["customer__phone", "customer__first_name", "specialist__first_name"]
    date_hierarchy = "date"
    list_editable = ["status"]
    readonly_fields = ["created_at", "updated_at"]
