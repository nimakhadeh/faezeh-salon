"""
Custom command to create default superuser
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Create default superuser if not exists"

    def handle(self, *args, **options):
        admin_phone = os.getenv("ADMIN_PHONE", "09399545113")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

        if not User.objects.filter(phone=admin_phone).exists():
            User.objects.create_superuser(
                username="admin",
                phone=admin_phone,
                password=admin_password,
                first_name="فائزه",
                last_name="مدیر",
                role="admin",
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {admin_phone}"))
        else:
            self.stdout.write(self.style.NOTICE("Superuser already exists."))
