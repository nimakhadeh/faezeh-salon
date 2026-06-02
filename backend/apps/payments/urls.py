"""
Payments URLs
"""

from django.urls import path
from .views import TransactionListView, PaymentRequestView, PaymentVerifyView

urlpatterns = [
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("request/", PaymentRequestView.as_view(), name="payment_request"),
    path("verify/", PaymentVerifyView.as_view(), name="payment_verify"),
]
