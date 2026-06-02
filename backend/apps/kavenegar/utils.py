"""
Kavenegar SMS Integration + Celery Tasks
"""

import requests
import logging
from django.conf import settings
from celery import shared_task

logger = logging.getLogger(__name__)


def get_kavenegar_api_key():
    return settings.KAVENEGAR.get("API_KEY", "")


def get_sender():
    return settings.KAVENEGAR.get("SENDER", "")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms(self, receptor, message):
    """Send SMS via Kavenegar API"""
    api_key = get_kavenegar_api_key()
    if not api_key:
        logger.warning("Kavenegar API key not configured. SMS not sent.")
        return {"success": False, "error": "API key not configured"}

    url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"
    params = {
        "receptor": receptor,
        "message": message,
    }
    sender = get_sender()
    if sender:
        params["sender"] = sender

    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if response.status_code == 200 and data.get("return", {}).get("status") == 200:
            logger.info(f"SMS sent to {receptor}: {data}")
            return {"success": True, "data": data}
        else:
            logger.error(f"Kavenegar error: {data}")
            return {"success": False, "error": str(data)}

    except requests.exceptions.RequestException as exc:
        logger.error(f"SMS request failed: {exc}")
        raise self.retry(exc=exc)


@shared_task
def send_appointment_reminder(appointment_id, hours_before):
    """Send appointment reminder SMS"""
    from apps.appointments.models import Appointment
    try:
        appt = Appointment.objects.get(id=appointment_id)
        customer = appt.customer
        service = appt.service
        specialist = appt.specialist

        if hours_before == 24:
            msg = (
                f"یادآوری نوبت فردا:\n"
                f"خدمت: {service.name}\n"
                f"تاریخ: {appt.date} ساعت {appt.start_time}\n"
                f"متخصص: {specialist.full_name}\n"
                f"آدرس: ستارخان کوچه ۱۲/۱\n"
                f"سالن فائزه - ۰۹۳۹۹۵۴۵۱۱۳"
            )
        elif hours_before == 2:
            msg = (
                f"یادآوری نوبت امروز:\n"
                f"خدمت: {service.name}\n"
                f"ساعت: {appt.start_time}\n"
                f"متخصص: {specialist.full_name}\n"
                f"آدرس: ستارخان کوچه ۱۲/۱\n"
                f"سالن فائزه - ۰۹۳۹۹۵۴۵۱۱۳"
            )
        else:
            return

        send_sms.delay(receptor=customer.phone, message=msg)

        if hours_before == 24:
            appt.reminder_24h_sent = True
        elif hours_before == 2:
            appt.reminder_2h_sent = True
        appt.save()

    except Appointment.DoesNotExist:
        logger.warning(f"Appointment {appointment_id} not found for reminder.")


@shared_task
def send_survey_request(appointment_id):
    """Send survey request after appointment completion"""
    from apps.appointments.models import Appointment
    try:
        appt = Appointment.objects.get(id=appointment_id)
        if appt.status != "completed":
            return

        msg = (
            f"{appt.customer.first_name} عزیز،\n"
            f"از اینکه سالن فائزه را انتخاب کردید متشکریم.\n"
            f"لطفاً با ثبت نظر خود به بهتر شدن ما کمک کنید:\n"
            f"لینک نظرسنجی: [لینک]\n"
            f"سالن فائزه"
        )
        send_sms.delay(receptor=appt.customer.phone, message=msg)
        appt.survey_sent = True
        appt.save()
    except Appointment.DoesNotExist:
        pass


@shared_task
def send_order_status_sms(order_id, status):
    """Send order status update SMS"""
    pass  # Implemented based on order model
