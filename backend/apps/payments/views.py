"""
Payments Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction

from .models import Transaction
from .serializers import TransactionSerializer, PaymentRequestSerializer, PaymentVerifySerializer
from .zarinpal import ZarinpalPayment
from apps.kavenegar.utils import send_sms
from apps.wallet.models import Wallet
from apps.appointments.models import Appointment


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)


class PaymentRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user

        # Create transaction record
        tx = Transaction.objects.create(
            user=user,
            amount=data["amount"],
            transaction_type=data["transaction_type"],
            description=data.get("description", ""),
            metadata=data.get("metadata", {}),
        )

        # Call Zarinpal
        zarinpal = ZarinpalPayment()
        callback = f"{request.build_absolute_uri('/api/payments/verify/')}"
        result = zarinpal.request_payment(
            amount=data["amount"],
            description=data.get("description", f"پرداخت {tx.get_transaction_type_display()}"),
            callback_url=callback,
            metadata={"transaction_id": tx.id, **data.get("metadata", {})},
        )

        if result["success"]:
            tx.authority = result["authority"]
            tx.save()
            return Response({
                "success": True,
                "payment_url": result["payment_url"],
                "authority": result["authority"],
                "transaction_id": tx.id,
            })
        else:
            tx.status = "failed"
            tx.save()
            return Response({"success": False, "error": result["error"]}, status=400)


class PaymentVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Handle Zarinpal callback (GET with authority and status params)"""
        authority = request.query_params.get("Authority")
        status_param = request.query_params.get("Status")

        if not authority:
            return Response({"success": False, "error": "Authority not provided."}, status=400)

        try:
            tx = Transaction.objects.get(authority=authority)
        except Transaction.DoesNotExist:
            return Response({"success": False, "error": "Transaction not found."}, status=404)

        if status_param != "OK":
            tx.status = "canceled"
            tx.save()
            return Response({"success": False, "error": "Payment canceled by user."})

        # Verify with Zarinpal
        zarinpal = ZarinpalPayment()
        result = zarinpal.verify_payment(authority=authority, amount=tx.amount)

        if result["success"]:
            with db_transaction.atomic():
                tx.status = "success"
                tx.ref_id = result.get("ref_id", "")
                tx.card_pan = result.get("card_pan", "")
                tx.save()

                # Handle based on transaction type
                self._handle_successful_payment(tx)

            return Response({
                "success": True,
                "message": result["message"],
                "ref_id": tx.ref_id,
                "transaction": TransactionSerializer(tx).data,
            })
        else:
            tx.status = "failed"
            tx.save()
            return Response({"success": False, "error": result["error"]}, status=400)

    def _handle_successful_payment(self, tx):
        """Handle side effects of successful payment"""
        metadata = tx.metadata

        if tx.transaction_type == "deposit":
            # Update appointment status
            appt_id = metadata.get("appointment_id")
            if appt_id:
                try:
                    appt = Appointment.objects.get(id=appt_id)
                    appt.status = "deposit_paid"
                    appt.save()
                except Appointment.DoesNotExist:
                    pass

        elif tx.transaction_type == "wallet_charge":
            # Add to wallet
            wallet, _ = Wallet.objects.get_or_create(user=tx.user)
            wallet.deposit(tx.amount, f"شارژ از طریق زرین‌پال - {tx.ref_id}")

        elif tx.transaction_type == "product":
            # Mark order as paid (handled in orders module)
            pass

        # Send SMS
        send_sms.delay(
            receptor=tx.user.phone,
            message=f"پرداخت شما با موفقیت انجام شد.\nمبلغ: {tx.amount:,} تومان\nکد پیگیری: {tx.ref_id}\nسالن فائزه"
        )


class PaymentVerifyPostView(APIView):
    """Alternative POST endpoint for verification"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Forward to GET handler logic
        request.query_params._mutable = True
        request.query_params["Authority"] = serializer.validated_data["authority"]
        request.query_params["Status"] = serializer.validated_data["status"]
        return PaymentVerifyView.as_view()(request._request)
