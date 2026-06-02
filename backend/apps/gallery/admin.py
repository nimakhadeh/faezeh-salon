"""
Gallery Admin
"""

from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["customer", "specialist", "service", "status", "is_public", "uploaded_at"]
    list_filter = ["status", "is_public", "uploaded_at"]
    list_editable = ["status", "is_public"]
    search_fields = ["customer__phone", "description"]
    readonly_fields = ["uploaded_at"]
