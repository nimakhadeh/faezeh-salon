"""
Loyalty Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import LoyaltyRule, LoyaltyPoint, LoyaltyTransaction
from .serializers import (
    LoyaltyRuleSerializer, LoyaltyPointSerializer,
    LoyaltyTransactionSerializer, ConvertPointsSerializer,
)
from apps.wallet.models import Wallet


class LoyaltyRuleListView(generics.ListAPIView):
    queryset = LoyaltyRule.objects.filter(is_active=True)
    serializer_class = LoyaltyRuleSerializer
    permission_classes = [permissions.AllowAny]


class MyLoyaltyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        points_obj, _ = LoyaltyPoint.objects.get_or_create(user=request.user)
        return Response(LoyaltyPointSerializer(points_obj).data)


class LoyaltyHistoryView(generics.ListAPIView):
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoyaltyTransaction.objects.filter(user=self.request.user)


class ConvertPointsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ConvertPointsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        points_to_convert = serializer.validated_data["points"]

        # Get active rule
        rule = LoyaltyRule.objects.filter(is_active=True).first()
        if not rule:
            return Response({"error": "هیچ قانون وفاداری فعالی وجود ندارد."}, status=400)

        points_obj, _ = LoyaltyPoint.objects.get_or_create(user=request.user)

        if points_obj.points < points_to_convert:
            return Response({"error": f"امتیاز ناکافی. شما {points_obj.points} امتیاز دارید."}, status=400)

        # Calculate amount
        conversion_ratio = rule.discount_amount / rule.points_to_discount
        wallet_amount = int(points_to_convert * conversion_ratio)

        try:
            points_obj.spend_points(
                points_to_convert,
                f"تبدیل به {wallet_amount:,} تومان در کیف پول"
            )
            wallet, _ = Wallet.objects.get_or_create(user=request.user)
            wallet.deposit(wallet_amount, f"تبدیل {points_to_convert} امتیاز وفاداری")

            return Response({
                "success": True,
                "message": f"{points_to_convert} امتیاز به {wallet_amount:,} تومان تبدیل شد.",
                "wallet_balance": wallet.balance,
                "remaining_points": points_obj.points,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)
