"""
Faezeh Salon - Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/services/", include("apps.services.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/wallet/", include("apps.wallet.urls")),
    path("api/loyalty/", include("apps.loyalty.urls")),
    path("api/gallery/", include("apps.gallery.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/survey/", include("apps.survey.urls")),
    path("api/crm/", include("apps.crm.urls")),
    path("telegram/", include("apps.telegram_bot.urls")),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
