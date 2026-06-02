"""
Appointments Serializers
"""

from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment
from apps.accounts.serializers import UserSerializer, SpecialistSerializer
from apps.services.serializers import ServiceListSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    specialist_name = serializers.CharField(source="specialist.full_name", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    service_type = serializers.CharField(source="service.get_braid_type_display", read_only=True)
    remaining_amount = serializers.ReadOnlyField()
    can_cancel = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = [
            "id", "customer", "specialist", "service",
            "customer_name", "specialist_name", "service_name", "service_type",
            "date", "start_time", "end_time", "status",
            "deposit_amount", "total_price", "final_price", "remaining_amount",
            "notes", "can_cancel", "is_upcoming",
            "created_at", "updated_at",
        ]
        read_only_fields = ["status", "deposit_amount", "total_price", "final_price"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["specialist", "service", "date", "start_time", "end_time", "notes"]

    def validate(self, data):
        # Check if date is in the future
        from datetime import datetime
        appt_datetime = datetime.combine(data["date"], data["start_time"])
        if appt_datetime < timezone.now():
            raise serializers.ValidationError("نمی‌توان نوبت را برای زمان گذشته رزرو کرد.")

        # Check if slot is at least 2 hours in advance
        if appt_datetime - timezone.now() < timedelta(hours=2):
            raise serializers.ValidationError("نوبت باید حداقل ۲ ساعت قبل رزرو شود.")

        # Calculate end_time from service duration if not provided
        if not data.get("end_time"):
            service = data["service"]
            start_dt = datetime.combine(data["date"], data["start_time"])
            end_dt = start_dt + timedelta(minutes=service.duration_minutes)
            data["end_time"] = end_dt.time()

        # Check overlapping
        overlapping = Appointment.objects.filter(
            specialist=data["specialist"],
            date=data["date"],
            status__in=["deposit_paid", "confirmed"],
        )
        for appt in overlapping:
            if (data["start_time"] < appt.end_time and data["end_time"] > appt.start_time):
                raise serializers.ValidationError("این بازه زمانی قبلاً رزرو شده است.")

        return data


class AvailableSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    is_available = serializers.BooleanField()


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status"]


class CustomerAppointmentHistorySerializer(serializers.ModelSerializer):
    service = ServiceListSerializer(read_only=True)
    specialist = SpecialistSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "date", "start_time", "service", "specialist", "status", "final_price"]
