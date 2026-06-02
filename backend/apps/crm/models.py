"""
CRM App - Simple Customer Relationship Management
"""

from django.db import models
from django.conf import settings


class CustomerInteraction(models.Model):
    INTERACTION_TYPES = [
        ("appointment", "نوبت"),
        ("purchase", "خرید"),
        ("chat", "چت"),
        ("survey", "نظرسنجی"),
        ("sms", "پیامک"),
        ("call", "تماس"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interactions",
        verbose_name="مشتری",
    )
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES, verbose_name="نوع")
    description = models.CharField(max_length=500, verbose_name="توضیحات")
    reference_id = models.CharField(max_length=100, blank=True, verbose_name="شناسه مرجع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "تعامل"
        verbose_name_plural = "تعاملات"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer} - {self.get_interaction_type_display()}"


class BulkSMS(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("sending", "در حال ارسال"),
        ("completed", "تکمیل شده"),
        ("failed", "ناموفق"),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان")
    message = models.TextField(verbose_name="متن پیامک")
    recipients = models.JSONField(default=list, verbose_name="گیرندگان")
    filter_criteria = models.JSONField(default=dict, blank=True, verbose_name="فیلترها")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "پیامک گروهی"
        verbose_name_plural = "پیامک‌های گروهی"

    def __str__(self):
        return self.title
