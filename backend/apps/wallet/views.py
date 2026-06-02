"""
Wallet Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction

from .models import Wallet, WalletTransaction
from .serializers import WalletSerializer, WalletTransactionSerializer
from apps.payments.models import Transaction
from apps.payments.zarinpal import ZarinpalPayment


class WalletDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return Response(WalletSerializer(wallet).data)


class WalletHistoryView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return wallet.transactions.all()


class WalletChargeView(APIView):
    """Initiate wallet charge via Zarinpal"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount", 0)
        try:
            amount = int(amount)
            if amount < 10000:
                return Response({"error": "حداقل مبلغ شارژ ۱۰,۰۰۰ تومان است."}, status=400)
        except ValueError:
            return Response({"error": "مبلغ نامعتبر."}, status=400)

        tx = Transaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type="wallet_charge",
            description=f"شارژ کیف پول - {amount:,} تومان",
            metadata={"wallet_charge": True},
        )

        zarinpal = ZarinpalPayment()
        result = zarinpal.request_payment(
            amount=amount,
            description=f"شارژ کیف پول سالن فائزه",
            callback_url=f"{request.build_absolute_uri('/api/payments/verify/')}",
            metadata={"transaction_id": tx.id},
        )

        if result["success"]:
            tx.authority = result["authority"]
            tx.save()
            return Response({
                "success": True,
                "payment_url": result["payment_url"],
                "authority": result["authority"],
            })
        return Response({"success": False, "error": result.get("error", "Payment request failed.")})


class WalletPaymentView(APIView):
    """Pay using wallet balance"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount", 0)
        description = request.data.get("description", "پرداخت از کیف پول")
        reference_type = request.data.get("reference_type")
        reference_id = request.data.get("reference_id")

        try:
            amount = int(amount)
        except ValueError:
            return Response({"error": "مبلغ نامعتبر."}, status=400)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        try:
            with db_transaction.atomic():
                wallet.withdraw(amount, description)
                # Create transaction record
                tx = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type="wallet_payment",
                    status="success",
                    description=description,
                    metadata={"reference_type": reference_type, "reference_id": reference_id},
                )
            return Response({
                "success": True,
                "message": "پرداخت با موفقیت انجام شد.",
                "remaining_balance": wallet.balance,
                "transaction": {"id": tx.id, "amount": amount},
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
