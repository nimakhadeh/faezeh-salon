"""
Chat App - 1:1 Chat between Customer and Specialist
"""

from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_rooms",
        verbose_name="مشتری",
    )
    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="specialist_rooms",
        verbose_name="متخصص",
        limit_choices_to={"role": "specialist"},
    )
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="chat_room",
        verbose_name="نوبت",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین پیام")

    class Meta:
        verbose_name = "اتاق چت"
        verbose_name_plural = "اتاق‌های چت"
        unique_together = ["customer", "specialist"]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.customer.full_name} - {self.specialist.full_name}"

    @property
    def last_message(self):
        return self.messages.order_by("-created_at").first()

    @property
    def unread_count(self, for_user=None):
        if for_user:
            return self.messages.exclude(sender=for_user).filter(is_read=False).count()
        return self.messages.filter(is_read=False).count()


class ChatMessage(models.Model):
    MSG_TYPE_CHOICES = [
        ("text", "متن"),
        ("image", "تصویر"),
        ("voice", "صدا"),
        ("file", "فایل"),
    ]

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="اتاق",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="فرستنده",
    )
    content = models.TextField(verbose_name="محتوا")
    message_type = models.CharField(max_length=10, choices=MSG_TYPE_CHOICES, default="text", verbose_name="نوع")
    file_url = models.URLField(blank=True, verbose_name="لینک فایل")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}"
