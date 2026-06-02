"""
Accounts App - Custom User Model with Customer/Specialist/Admin roles
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os


def user_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"avatars/user_{instance.id}.{ext}"


class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "مشتری"),
        ("specialist", "متخصص"),
        ("admin", "مدیر"),
    ]

    GENDER_CHOICES = [
        ("female", "خانم"),
        ("male", "آقا"),
    ]

    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message="شماره موبایل باید ۱۱ رقم و با ۰۹ شروع شود."
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer", verbose_name="نقش")
    phone = models.CharField(max_length=11, validators=[phone_regex], unique=True, verbose_name="موبایل")
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, verbose_name="عکس پروفایل")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name="جنسیت")
    instagram = models.CharField(max_length=100, blank=True, verbose_name="اینستاگرام")
    address = models.TextField(blank=True, verbose_name="آدرس")
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    # Specialist fields
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="سال تجربه")
    work_hours_start = models.TimeField(default="10:00:00", verbose_name="ساعت شروع کار")
    work_hours_end = models.TimeField(default="20:00:00", verbose_name="ساعت پایان کار")
    work_days = models.JSONField(default=list, verbose_name="روزهای کاری")  # [0,1,2,3,4,5] Sat=0
    is_available = models.BooleanField(default=True, verbose_name="در دسترس")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.phone

    @property
    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    @property
    def is_specialist(self):
        return self.role == "specialist"

    @property
    def is_admin_role(self):
        return self.role == "admin"


class PasswordResetOTP(models.Model):
    phone = models.CharField(max_length=11, verbose_name="موبایل")
    code = models.CharField(max_length=6, verbose_name="کد OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")

    class Meta:
        verbose_name = "کد بازنشانی رمز"
        verbose_name_plural = "کدهای بازنشانی رمز"

    def __str__(self):
        return f"{self.phone} - {self.code}"
