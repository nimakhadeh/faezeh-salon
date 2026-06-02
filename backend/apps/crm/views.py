"""
CRM Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q, Max, Avg, F
from django.contrib.auth import get_user_model

from .models import CustomerInteraction, BulkSMS
from .serializers import CustomerInteractionSerializer, BulkSMSSerializer, CustomerSummarySerializer
from apps.kavenegar.utils import send_sms

User = get_user_model()


class CustomerListView(APIView):
    """Admin: List customers with summary stats"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        min_appointments = request.query_params.get("min_appointments")
        max_appointments = request.query_params.get("max_appointments")
        has_visit_after = request.query_params.get("has_visit_after")
        has_visit_before = request.query_params.get("has_visit_before")

        users = User.objects.filter(role="customer")

        if min_appointments:
            users = users.annotate(appt_count=Count("customer_appointments")).filter(appt_count__gte=int(min_appointments))
        if max_appointments:
            users = users.annotate(appt_count=Count("customer_appointments")).filter(appt_count__lte=int(max_appointments))

        users = users.annotate(
            total_appointments=Count("customer_appointments", distinct=True),
            total_spent=Sum("customer_appointments__final_price", distinct=True),
            last_visit=Max("customer_appointments__date"),
        ).order_by("-total_spent")

        results = []
        for u in users:
            points = getattr(u, "loyalty_points", None)
            results.append({
                "id": u.id,
                "full_name": u.full_name,
                "phone": u.phone,
                "total_appointments": u.total_appointments or 0,
                "total_spent": u.total_spent or 0,
                "last_visit": u.last_visit,
                "loyalty_points": points.points if points else 0,
            })

        return Response(results)


class CustomerDetailView(APIView):
    """Admin: Customer detail with full history"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, role="customer")
        except User.DoesNotExist:
            return Response({"error": "Customer not found."}, status=404)

        # Appointments
        appointments = user.customer_appointments.all()
        appointments_data = []
        for a in appointments:
            appointments_data.append({
                "id": a.id,
                "date": a.date,
                "service": a.service.name if a.service else None,
                "status": a.status,
                "amount": a.final_price,
            })

        # Purchases (transactions)
        transactions = user.transactions.filter(status="success")
        transactions_data = []
        for t in transactions:
            transactions_data.append({
                "id": t.id,
                "type": t.transaction_type,
                "amount": t.amount,
                "date": t.created_at,
            })

        # Chat rooms
        chat_rooms = user.customer_rooms.all()
        chats_data = []
        for c in chat_rooms:
            chats_data.append({
                "id": c.id,
                "specialist": c.specialist.full_name,
                "message_count": c.messages.count(),
            })

        # Surveys
        surveys = user.surveys.all()
        surveys_data = []
        for s in surveys:
            surveys_data.append({
                "id": s.id,
                "nps_score": s.nps_score,
                "comment": s.comment,
                "date": s.created_at,
            })

        # Interactions
        interactions = CustomerInteraction.objects.filter(customer=user)
        interactions_data = CustomerInteractionSerializer(interactions, many=True).data

        return Response({
            "customer": {
                "id": user.id,
                "name": user.full_name,
                "phone": user.phone,
                "email": user.email,
                "birth_date": user.birth_date,
                "registered_at": user.created_at,
            },
            "appointments": appointments_data,
            "transactions": transactions_data,
            "chats": chats_data,
            "surveys": surveys_data,
            "interactions": interactions_data,
        })


class CustomerInteractionListView(generics.ListCreateAPIView):
    queryset = CustomerInteraction.objects.all()
    serializer_class = CustomerInteractionSerializer
    permission_classes = [permissions.IsAdminUser]


class BulkSMSCreateView(APIView):
    """Admin: Send bulk SMS"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        title = request.data.get("title")
        message = request.data.get("message")
        phones = request.data.get("phones", [])
        send_to_all = request.data.get("send_to_all", False)

        if not message:
            return Response({"error": "Message is required."}, status=400)

        if send_to_all:
            phones = list(User.objects.filter(role="customer").values_list("phone", flat=True))

        if not phones:
            return Response({"error": "No recipients."}, status=400)

        bulk = BulkSMS.objects.create(
            title=title or "پیامک گروهی",
            message=message,
            recipients=phones,
            created_by=request.user,
        )

        # Send via Celery
        for phone in phones:
            send_sms.delay(receptor=phone, message=message)

        bulk.status = "completed"
        bulk.sent_count = len(phones)
        bulk.save()

        return Response({
            "success": True,
            "sent_count": len(phones),
            "bulk_id": bulk.id,
        })
