"""
Services Views
"""

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Service, Product
from .serializers import (
    CategorySerializer, ServiceListSerializer, ServiceDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["braid_type", "category", "requires_deposit"]
    search_fields = ["name", "description"]
    ordering_fields = ["base_price", "duration_minutes", "created_at"]


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    lookup_field = "slug"


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_featured", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class FeaturedProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True, is_featured=True)
    serializer_class = ProductListSerializer
