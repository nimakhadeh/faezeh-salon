"""
Gallery App - Before/After Photos
"""

from django.db import models
from django.conf import settings


class GalleryImage(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار تأیید"),
        ("approved", "تأیید شده"),
        ("rejected", "رد شده"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gallery_uploads",
        verbose_name="مشتری",
    )
    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="specialist_gallery",
        verbose_name="متخصص",
        limit_choices_to={"role": "specialist"},
        null=True,
        blank=True,
    )
    image_before = models.ImageField(upload_to="gallery/before/", verbose_name="تصویر قبل")
    image_after = models.ImageField(upload_to="gallery/after/", verbose_name="تصویر بعد")
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gallery_images",
        verbose_name="خدمت",
    )
    description = models.TextField(blank=True, verbose_name="توضیحات")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="وضعیت")
    is_public = models.BooleanField(default=False, verbose_name="عمومی")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ بررسی")
    review_note = models.TextField(blank=True, verbose_name="یادداشت بررسی")

    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "تصاویر گالری"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.customer.full_name} - {self.service.name if self.service else 'بدون خدمت'}"
