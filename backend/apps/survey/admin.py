"""
Survey Admin
"""

from django.contrib import admin
from .models import SurveyResponse


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ["customer", "specialist", "nps_score", "nps_category", "created_at"]
    list_filter = ["nps_score", "created_at"]
    search_fields = ["customer__phone", "comment"]
    readonly_fields = ["created_at"]

    @admin.display(description="دسته NPS")
    def nps_category(self, obj):
        return obj.nps_category
