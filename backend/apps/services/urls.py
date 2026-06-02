"""
Services URLs
"""

from django.urls import path
from .views import (
    CategoryListView,
    ServiceListView, ServiceDetailView,
    ProductListView, ProductDetailView, FeaturedProductListView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("services/", ServiceListView.as_view(), name="services"),
    path("services/<slug:slug>/", ServiceDetailView.as_view(), name="service_detail"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/featured/", FeaturedProductListView.as_view(), name="featured_products"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]
