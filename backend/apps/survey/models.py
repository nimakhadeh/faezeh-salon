"""
Survey App - NPS + Targeted Questions
"""

from django.db import models
from django.conf import settings


class SurveyResponse(models.Model):
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="survey",
        verbose_name="نوبت",
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="surveys",
        verbose_name="مشتری",
    )
    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_surveys",
        verbose_name="متخصص",
        limit_choices_to={"role": "specialist"},
    )
    nps_score = models.PositiveIntegerField(
        verbose_name="امتیاز NPS (۰-۱۰)",
        help_text="۰ = هرگز، ۱۰ = قطعاً",
    )
    satisfaction_question = models.CharField(
        max_length=500,
        default="کدام بخش بیشتر راضی بودید؟",
        verbose_name="سوال رضایت",
    )
    satisfaction_answer = models.CharField(max_length=500, blank=True, verbose_name="پاسخ رضایت")
    comment = models.TextField(blank=True, verbose_name="نظر آزاد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "پاسخ نظرسنجی"
        verbose_name_plural = "پاسخ‌های نظرسنجی"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer} - NPS: {self.nps_score}"

    @property
    def nps_category(self):
        if self.nps_score >= 9:
            return "promoter"
        elif self.nps_score >= 7:
            return "passive"
        return "detractor"
