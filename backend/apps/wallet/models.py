"""
Wallet App - Internal Wallet System
"""

from django.db import models
from django.conf import settings


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name="کاربر",
    )
    balance = models.PositiveIntegerField(default=0, verbose_name="موجودی (تومان)")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول‌ها"

    def __str__(self):
        return f"{self.user.full_name} - {self.balance:,} تومان"

    def deposit(self, amount, description=""):
        """Add funds to wallet"""
        self.balance += amount
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type="deposit",
            description=description,
        )
        return self.balance

    def withdraw(self, amount, description=""):
        """Deduct funds from wallet"""
        if self.balance < amount:
            raise ValueError("موجودی ناکافی")
        self.balance -= amount
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type="withdraw",
            description=description,
        )
        return self.balance


class WalletTransaction(models.Model):
    TYPE_CHOICES = [
        ("deposit", "واریز"),
        ("withdraw", "برداشت"),
        ("refund", "بازگشت وجه"),
        ("loyalty_convert", "تبدیل امتیاز"),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="کیف پول",
    )
    amount = models.PositiveIntegerField(verbose_name="مبلغ (تومان)")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="نوع")
    description = models.CharField(max_length=500, blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "تراکنش کیف پول"
        verbose_name_plural = "تراکنش‌های کیف پول"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.wallet.user} - {self.get_transaction_type_display()} {self.amount:,}"
