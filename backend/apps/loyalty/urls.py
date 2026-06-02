"""
Loyalty URLs
"""

from django.urls import path
from .views import LoyaltyRuleListView, MyLoyaltyView, LoyaltyHistoryView, ConvertPointsView

urlpatterns = [
    path("rules/", LoyaltyRuleListView.as_view(), name="loyalty_rules"),
    path("my/", MyLoyaltyView.as_view(), name="my_loyalty"),
    path("history/", LoyaltyHistoryView.as_view(), name="loyalty_history"),
    path("convert/", ConvertPointsView.as_view(), name="convert_points"),
]
