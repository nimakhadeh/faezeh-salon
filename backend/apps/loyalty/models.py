"""
Loyalty App - Points System
"""

from django.db import models
from django.conf import settings


class LoyaltyRule(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام قانون")
    points_per_amount = models.PositiveIntegerField(default=1, verbose_name="امتیاز به ازای هر (تومان)")
    amount_threshold = models.PositiveIntegerField(default=1000, verbose_name="حد آستانه (تومان)")
    points_to_discount = models.PositiveIntegerField(default=10, verbose_name="امتیاز لازم برای تخفیف")
    discount_amount = models.PositiveIntegerField(default=1000, verbose_name="مبلغ تخفیف (تومان)")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "قانون وفاداری"
        verbose_name_plural = "قوانین وفاداری"

    def __str__(self):
        return self.name

    def calculate_points(self, amount):
        """Calculate points for a given amount"""
        return (amount // self.amount_threshold) * self.points_per_amount


class LoyaltyPoint(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loyalty_points",
        verbose_name="کاربر",
    )
    points = models.PositiveIntegerField(default=0, verbose_name="امتیاز")
    total_earned = models.PositiveIntegerField(default=0, verbose_name="کل امتیاز کسب شده")
    total_spent = models.PositiveIntegerField(default=0, verbose_name="کل امتیاز مصرف شده")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "امتیاز وفاداری"
        verbose_name_plural = "امتیازهای وفاداری"

    def __str__(self):
        return f"{self.user.full_name} - {self.points} امتیاز"

    def add_points(self, points, description=""):
        self.points += points
        self.total_earned += points
        self.save()
        LoyaltyTransaction.objects.create(
            user=self.user,
            points=points,
            transaction_type="earn",
            description=description,
        )

    def spend_points(self, points, description=""):
        if self.points < points:
            raise ValueError("امتیاز ناکافی")
        self.points -= points
        self.total_spent += points
        self.save()
        LoyaltyTransaction.objects.create(
            user=self.user,
            points=points,
            transaction_type="spend",
            description=description,
        )


class LoyaltyTransaction(models.Model):
    TYPE_CHOICES = [
        ("earn", "کسب امتیاز"),
        ("spend", "مصرف امتیاز"),
        ("expire", "انقضا"),
        ("bonus", "جایزه"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loyalty_transactions",
        verbose_name="کاربر",
    )
    points = models.IntegerField(verbose_name="امتیاز")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="نوع")
    description = models.CharField(max_length=500, blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تراکنش امتیاز"
        verbose_name_plural = "تراکنش‌های امتیاز"
        ordering = ["-created_at"]

    def __str__(self):
        sign = "+" if self.transaction_type == "earn" else "-"
        return f"{self.user} - {sign}{self.points}"
