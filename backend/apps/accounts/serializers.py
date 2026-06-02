"""
Accounts Serializers
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "full_name",
            "phone", "email", "avatar", "birth_date", "age", "gender",
            "instagram", "address", "role", "bio", "experience_years",
            "work_hours_start", "work_hours_end", "work_days",
            "is_available", "is_verified", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "role", "is_verified", "created_at", "updated_at"]


class SpecialistSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    rating = serializers.SerializerMethodField()
    appointment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "full_name",
            "phone", "avatar", "bio", "experience_years",
            "work_hours_start", "work_hours_end", "work_days",
            "is_available", "rating", "appointment_count",
        ]

    def get_rating(self, obj):
        from apps.survey.models import SurveyResponse
        responses = SurveyResponse.objects.filter(appointment__specialist=obj)
        if responses.exists():
            return round(responses.filter(nps_score__gte=9).count() / responses.count() * 100, 1)
        return 0.0

    def get_appointment_count(self, obj):
        return obj.specialist_appointments.filter(status="completed").count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone", "username", "first_name", "last_name", "password", "password2", "role"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "رمز عبور و تکرار آن یکسان نیستند."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["phone"] = user.phone
        token["role"] = user.role
        token["full_name"] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password": "رمز عبور جدید و تکرار آن یکسان نیستند."})
        return attrs


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=11)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=11)
    code = serializers.CharField(required=True, max_length=6)
    new_password = serializers.CharField(required=True)
