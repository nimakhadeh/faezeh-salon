"""
Services Serializers
"""

from rest_framework import serializers
from .models import Category, Service, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon", "is_active"]


class ServiceListSerializer(serializers.ModelSerializer):
    braid_type_display = serializers.CharField(source="get_braid_type_display", read_only=True)
    price_range = serializers.ReadOnlyField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Service
        fields = [
            "id", "name", "slug", "description", "braid_type",
            "braid_type_display", "duration_minutes", "price_range",
            "base_price", "max_price", "image", "is_active",
            "suitable_ages", "requires_deposit", "deposit_percent",
            "category", "category_name",
        ]


class ServiceDetailSerializer(serializers.ModelSerializer):
    braid_type_display = serializers.CharField(source="get_braid_type_display", read_only=True)
    price_range = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    has_discount = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price",
            "discount_price", "final_price", "has_discount",
            "discount_percent", "stock", "is_in_stock",
            "image", "is_active", "is_featured",
            "category", "category_name",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
