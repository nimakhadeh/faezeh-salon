"""
Appointments Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db.models import Q

from .models import Appointment
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer,
    AvailableSlotSerializer, AppointmentStatusUpdateSerializer,
    CustomerAppointmentHistorySerializer,
)
from apps.accounts.models import User
from apps.services.models import Service
from apps.payments.models import Transaction
from apps.payments.zarinpal import ZarinpalPayment
from apps.kavenegar.utils import send_sms


class AvailableSlotsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        specialist_id = request.query_params.get("specialist")
        service_id = request.query_params.get("service")
        date_str = request.query_params.get("date")

        if not all([specialist_id, service_id, date_str]):
            return Response({"error": "specialist, service, date are required."}, status=400)

        try:
            specialist = User.objects.get(id=specialist_id, role="specialist")
            service = Service.objects.get(id=service_id)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (User.DoesNotExist, Service.DoesNotExist, ValueError):
            return Response({"error": "Invalid parameters."}, status=400)

        # Check if date is a working day
        weekday = date.weekday()
        if specialist.work_days and weekday not in specialist.work_days:
            return Response({"slots": [], "message": "متخصص در این روز کار نمی‌کند."})

        # Generate 30-minute time slots
        slots = []
        current_time = specialist.work_hours_start
        end_time = specialist.work_hours_end

        # Get booked slots
        booked = Appointment.objects.filter(
            specialist=specialist,
            date=date,
            status__in=["deposit_paid", "confirmed"],
        ).values_list("start_time", "end_time")

        while current_time < end_time:
            slot_end = (datetime.combine(date, current_time) + timedelta(minutes=service.duration_minutes)).time()
            if slot_end > end_time:
                break

            is_available = not any(
                current_time < booked_end and slot_end > booked_start
                for booked_start, booked_end in booked
            )

            slots.append({
                "start_time": current_time.strftime("%H:%M"),
                "end_time": slot_end.strftime("%H:%M"),
                "is_available": is_available,
            })

            current_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()

        return Response({"slots": slots})


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Appointment.objects.all()
        elif user.role == "specialist":
            return Appointment.objects.filter(specialist=user)
        return Appointment.objects.filter(customer=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save(customer=self.request.user)
        # Create deposit transaction
        if appointment.service.requires_deposit:
            transaction = Transaction.objects.create(
                user=self.request.user,
                amount=appointment.deposit_amount,
                transaction_type="deposit",
                reference_id=f"appt_deposit_{appointment.id}",
                metadata={"appointment_id": appointment.id},
            )
            # Generate payment URL
            zarinpal = ZarinpalPayment()
            result = zarinpal.request_payment(
                amount=appointment.deposit_amount,
                description=f"بیعانه نوبت {appointment.service.name}",
                callback_url=f"{request.build_absolute_uri('/api/payments/verify/')}",
                metadata={"appointment_id": appointment.id, "transaction_id": transaction.id},
            )
            if result.get("success"):
                transaction.authority = result["authority"]
                transaction.save()
                # Return payment URL in response
                self.payment_url = result["payment_url"]
            else:
                self.payment_url = None

        # Send SMS confirmation
        send_sms.delay(
            receptor=appointment.customer.phone,
            message=f"نوبت شما ثبت شد.\nخدمت: {appointment.service.name}\nتاریخ: {appointment.date} ساعت {appointment.start_time}\nلطفاً بیعانه را پرداخت کنید."
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = AppointmentSerializer(serializer.instance).data
        if hasattr(self, "payment_url") and self.payment_url:
            response_data["payment_url"] = self.payment_url
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Appointment.objects.all()
        elif user.role == "specialist":
            return Appointment.objects.filter(specialist=user)
        return Appointment.objects.filter(customer=user)

    def perform_destroy(self, instance):
        if not instance.can_cancel:
            raise permissions.PermissionDenied("امکان لغو نوبت کمتر از ۶ ساعت قبل وجود ندارد.")
        instance.status = "canceled"
        instance.save()
        send_sms.delay(
            receptor=instance.customer.phone,
            message=f"نوبت شما لغو شد.\nخدمت: {instance.service.name}\nتاریخ: {instance.date} {instance.start_time}"
        )


class AppointmentStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            if user.role == "admin":
                appointment = Appointment.objects.get(pk=pk)
            elif user.role == "specialist":
                appointment = Appointment.objects.get(pk=pk, specialist=user)
            else:
                appointment = Appointment.objects.get(pk=pk, customer=user)
        except Appointment.DoesNotExist:
            return Response({"error": "نوبت یافت نشد."}, status=404)

        new_status = request.data.get("status")
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({"error": "وضعیت نامعتبر."}, status=400)

        appointment.status = new_status
        appointment.save()

        # Send status change SMS
        status_display = dict(Appointment.STATUS_CHOICES).get(new_status, new_status)
        send_sms.delay(
            receptor=appointment.customer.phone,
            message=f"وضعیت نوبت شما تغییر کرد: {status_display}\nخدمت: {appointment.service.name}\nتاریخ: {appointment.date} {appointment.start_time}"
        )

        return Response(AppointmentSerializer(appointment).data)


class MyAppointmentsView(generics.ListAPIView):
    serializer_class = CustomerAppointmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(customer=self.request.user).order_by("-date", "-start_time")


class SpecialistScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_specialist:
            return Response({"error": "Only specialists can view their schedule."}, status=403)

        date_str = request.query_params.get("date")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            appointments = Appointment.objects.filter(
                specialist=request.user,
                date=date,
                status__in=["deposit_paid", "confirmed", "completed"],
            )
        else:
            appointments = Appointment.objects.filter(
                specialist=request.user,
                date__gte=timezone.now().date(),
                status__in=["deposit_paid", "confirmed", "completed"],
            ).order_by("date", "start_time")

        return Response(AppointmentSerializer(appointments, many=True).data)
