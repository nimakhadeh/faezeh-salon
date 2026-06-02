"""
CRM URLs
"""

from django.urls import path
from .views import (
    CustomerListView, CustomerDetailView,
    CustomerInteractionListView, BulkSMSCreateView,
)

urlpatterns = [
    path("customers/", CustomerListView.as_view(), name="crm_customers"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="crm_customer_detail"),
    path("interactions/", CustomerInteractionListView.as_view(), name="crm_interactions"),
    path("bulk-sms/", BulkSMSCreateView.as_view(), name="crm_bulk_sms"),
]
