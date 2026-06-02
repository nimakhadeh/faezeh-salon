"""
Accounts Admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["phone", "full_name", "role", "is_verified", "is_active", "created_at"]
    list_filter = ["role", "is_verified", "is_active", "gender", "created_at"]
    search_fields = ["phone", "first_name", "last_name", "username"]
    ordering = ["-created_at"]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("اطلاعات سالن", {
            "fields": ("role", "phone", "avatar", "birth_date", "gender", "instagram", "address", "is_verified"),
        }),
        ("اطلاعات متخصص", {
            "fields": ("bio", "experience_years", "work_hours_start", "work_hours_end", "work_days", "is_available"),
            "classes": ("collapse",),
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("اطلاعات اضافی", {
            "fields": ("phone", "role", "first_name", "last_name"),
        }),
    )

    @admin.display(description="نام کامل")
    def full_name(self, obj):
        return obj.full_name


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "is_used", "created_at"]
    list_filter = ["is_used", "created_at"]
    search_fields = ["phone", "code"]
    readonly_fields = ["created_at"]
