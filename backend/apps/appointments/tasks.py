"""
Appointments Celery Tasks - Reminders and follow-ups
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Appointment
from apps.kavenegar.utils import send_sms, send_appointment_reminder, send_survey_request


@shared_task
def send_appointment_reminders_24h():
    """Send 24-hour reminders - runs every hour via Celery Beat"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        date=tomorrow,
        status__in=["deposit_paid", "confirmed"],
        reminder_24h_sent=False,
    )
    for appt in appointments:
        send_appointment_reminder.delay(appt.id, 24)


@shared_task
def send_appointment_reminders_2h():
    """Send 2-hour reminders - runs every hour via Celery Beat"""
    now = timezone.now()
    in_2h = now + timedelta(hours=2)
    today = now.date()

    appointments = Appointment.objects.filter(
        date=today,
        status__in=["deposit_paid", "confirmed"],
        reminder_2h_sent=False,
        start_time__hour=in_2h.hour,
    )
    for appt in appointments:
        send_appointment_reminder.delay(appt.id, 2)


@shared_task
def complete_past_appointments():
    """Auto-mark past appointments as completed"""
    now = timezone.now()
    Appointment.objects.filter(
        date__lt=now.date(),
        status__in=["deposit_paid", "confirmed"],
    ).update(status="completed")

    # Also mark today's past appointments
    Appointment.objects.filter(
        date=now.date(),
        end_time__lt=now.time(),
        status__in=["deposit_paid", "confirmed"],
    ).update(status="completed")


@shared_task
def send_survey_requests():
    """Send survey requests for completed appointments without surveys"""
    from django.db.models import Count
    completed_appts = Appointment.objects.filter(
        status="completed",
        survey_sent=False,
    )
    for appt in completed_appts:
        send_survey_request.delay(appt.id)
