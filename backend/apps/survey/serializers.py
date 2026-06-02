"""
Survey Serializers
"""

from rest_framework import serializers
from .models import SurveyResponse


class SurveyResponseSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    specialist_name = serializers.CharField(source="specialist.full_name", read_only=True)
    nps_category = serializers.ReadOnlyField()

    class Meta:
        model = SurveyResponse
        fields = [
            "id", "appointment", "customer", "customer_name",
            "specialist", "specialist_name", "nps_score",
            "satisfaction_question", "satisfaction_answer",
            "comment", "nps_category", "created_at",
        ]
        read_only_fields = ["customer", "specialist"]


class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ["appointment", "nps_score", "satisfaction_answer", "comment"]

    def validate_nps_score(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError("امتیاز باید بین ۰ و ۱۰ باشد.")
        return value

    def validate(self, data):
        appointment = data["appointment"]
        if appointment.customer != self.context["request"].user:
            raise serializers.ValidationError("شما مجاز به ثبت نظرسنجی برای این نوبت نیستید.")
        if appointment.status != "completed":
            raise serializers.ValidationError("نوبت هنوز تکمیل نشده است.")
        return data

    def create(self, validated_data):
        appointment = validated_data["appointment"]
        return SurveyResponse.objects.create(
            appointment=appointment,
            customer=appointment.customer,
            specialist=appointment.specialist,
            **validated_data,
        )


class SurveyStatsSerializer(serializers.Serializer):
    total_surveys = serializers.IntegerField()
    avg_nps = serializers.FloatField()
    promoters = serializers.IntegerField()
    passives = serializers.IntegerField()
    detractors = serializers.IntegerField()
    nps_score = serializers.FloatField()
