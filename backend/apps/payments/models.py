"""
Payments App - Transaction Model
"""

from django.db import models
from django.conf import settings


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("deposit", "بیعانه نوبت"),
        ("product", "خرید محصول"),
        ("service", "خرید خدمت"),
        ("wallet_charge", "شارژ کیف پول"),
        ("wallet_payment", "پرداخت با کیف پول"),
        ("refund", "بازگشت وجه"),
    ]

    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("success", "موفق"),
        ("failed", "ناموفق"),
        ("canceled", "لغو شده"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="کاربر",
    )
    amount = models.PositiveIntegerField(verbose_name="مبلغ (تومان)")
    transaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="نوع تراکنش",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت",
    )
    authority = models.CharField(max_length=50, blank=True, verbose_name="کد authority")
    ref_id = models.CharField(max_length=100, blank=True, verbose_name="کد مرجع")
    reference_id = models.CharField(max_length=100, blank=True, verbose_name="شناسه داخلی")
    description = models.CharField(max_length=500, blank=True, verbose_name="توضیحات")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="متادیتا")
    card_pan = models.CharField(max_length=20, blank=True, verbose_name="شماره کارت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.amount:,} - {self.get_transaction_type_display()}"
