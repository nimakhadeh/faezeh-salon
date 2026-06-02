"""
Appointments App - Booking with calendar, time slots, and deposit payment
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("deposit_paid", "بیعانه پرداخت شده"),
        ("confirmed", "تأیید شده"),
        ("completed", "انجام شده"),
        ("canceled", "لغو شده"),
        ("no_show", "عدم مراجعه"),
    ]

    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="customer_appointments",
        verbose_name="مشتری",
    )
    specialist = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="specialist_appointments",
        verbose_name="متخصص",
        limit_choices_to={"role": "specialist"},
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="خدمت",
    )
    date = models.DateField(verbose_name="تاریخ")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت",
    )
    deposit_amount = models.PositiveIntegerField(default=0, verbose_name="مبلغ بیعانه (تومان)")
    total_price = models.PositiveIntegerField(default=0, verbose_name="قیمت کل (تومان)")
    final_price = models.PositiveIntegerField(default=0, verbose_name="مبلغ نهایی (تومان)")
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    reminder_24h_sent = models.BooleanField(default=False, verbose_name="یادآوری ۲۴ ساعته ارسال شد")
    reminder_2h_sent = models.BooleanField(default=False, verbose_name="یادآوری ۲ ساعته ارسال شد")
    survey_sent = models.BooleanField(default=False, verbose_name="نظرسنجی ارسال شد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"
        ordering = ["-date", "-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "date", "start_time"],
                name="unique_time_slot",
            ),
        ]

    def __str__(self):
        return f"{self.customer.full_name} - {self.service.name} - {self.date} {self.start_time}"

    def clean(self):
        # Check if end_time is after start_time
        if self.end_time <= self.start_time:
            raise ValidationError("ساعت پایان باید بعد از ساعت شروع باشد.")

        # Check specialist work days
        weekday = self.date.weekday()
        if self.specialist.work_days and weekday not in self.specialist.work_days:
            raise ValidationError("متخصص در این روز کار نمی‌کند.")

        # Check specialist work hours
        if self.start_time < self.specialist.work_hours_start or self.end_time > self.specialist.work_hours_end:
            raise ValidationError("زمان انتخابی خارج از ساعت کاری متخصص است.")

        # Check for overlapping appointments (excluding self)
        overlapping = Appointment.objects.filter(
            specialist=self.specialist,
            date=self.date,
            status__in=["deposit_paid", "confirmed"],
        ).exclude(id=self.id)

        for appt in overlapping:
            if (self.start_time < appt.end_time and self.end_time > appt.start_time):
                raise ValidationError("این بازه زمانی با نوبت دیگری تداخل دارد.")

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.service.base_price
        if not self.final_price:
            self.final_price = self.total_price
        if self.service.requires_deposit and not self.deposit_amount:
            self.deposit_amount = int(self.total_price * self.service.deposit_percent / 100)
        self.clean()
        super().save(*args, **kwargs)

    @property
    def remaining_amount(self):
        return self.final_price - self.deposit_amount

    @property
    def is_upcoming(self):
        from datetime import datetime
        appt_datetime = datetime.combine(self.date, self.start_time)
        return appt_datetime > timezone.now()

    @property
    def can_cancel(self):
        from datetime import datetime, timedelta
        appt_datetime = datetime.combine(self.date, self.start_time)
        return appt_datetime - timezone.now() > timedelta(hours=6)
