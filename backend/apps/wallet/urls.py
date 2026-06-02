"""
Wallet URLs
"""

from django.urls import path
from .views import WalletDetailView, WalletHistoryView, WalletChargeView, WalletPaymentView

urlpatterns = [
    path("", WalletDetailView.as_view(), name="wallet"),
    path("history/", WalletHistoryView.as_view(), name="wallet_history"),
    path("charge/", WalletChargeView.as_view(), name="wallet_charge"),
    path("pay/", WalletPaymentView.as_view(), name="wallet_pay"),
]
