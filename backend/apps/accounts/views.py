"""
Accounts Views - Auth, Profile, Password Management
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import random

from .serializers import (
    UserSerializer, SpecialistSerializer, RegisterSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    RequestOTPSerializer, VerifyOTPSerializer,
)
from .models import PasswordResetOTP
from apps.kavenegar.utils import send_sms

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Send welcome SMS
        send_sms.delay(
            receptor=user.phone,
            message=f"{user.first_name} عزیز، به سالن فائزه خوش آمدید! \nظ\u0631\u0641\u062a\u060c \u062f\u0648\u0627\u0645 \u0628\u0627\u0644\u0627\u060c \u062d\u0627\u0644 \u062e\u0648\u0628 \u060c \u0627\u0639\u062a\u0645\u0627\u062f \u0628\u0647 \u0646\u0641\u0633"
        )
        return Response({
            "message": "ثبت‌نام با موفقیت انجام شد.",
            "user": UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SpecialistListView(generics.ListAPIView):
    queryset = User.objects.filter(role="specialist", is_active=True)
    serializer_class = SpecialistSerializer
    permission_classes = [permissions.AllowAny]


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "رمز عبور فعلی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "رمز عبور با موفقیت تغییر کرد."})


class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"phone": "این شماره موبایل ثبت نشده است."}, status=status.HTTP_404_NOT_FOUND)

        # Delete old OTPs
        PasswordResetOTP.objects.filter(phone=phone, is_used=False).delete()

        # Generate 6-digit code
        code = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(phone=phone, code=code)

        # Send SMS via Kavenegar
        send_sms.delay(
            receptor=phone,
            message=f"کد بازنشانی رمز عبور سالن فائزه:\n{code}\nاین کد ۱۰ دقیقه اعتبار دارد."
        )

        return Response({"message": "کد تأیید ارسال شد.", "phone": phone})


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]

        try:
            otp = PasswordResetOTP.objects.filter(
                phone=phone,
                code=code,
                is_used=False,
                created_at__gte=timezone.now() - timedelta(minutes=10)
            ).latest("created_at")
        except PasswordResetOTP.DoesNotExist:
            return Response({"code": "کد نامعتبر یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"phone": "کاربر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        otp.is_used = True
        otp.save()

        return Response({"message": "رمز عبور با موفقیت بازنشانی شد."})
