"""
Services Admin
"""

from django.contrib import admin
from .models import Category, Service, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "order", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "braid_type", "base_price", "duration_minutes", "is_active", "requires_deposit"]
    list_filter = ["braid_type", "is_active", "requires_deposit", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_active"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "discount_price", "stock", "is_active", "is_featured"]
    list_filter = ["is_active", "is_featured", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_active", "is_featured"]
