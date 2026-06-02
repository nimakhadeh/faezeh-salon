"""
Telegram Bot Webhook View
"""

import json
import logging
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        if not settings.TELEGRAM_BOT_TOKEN:
            return JsonResponse({"ok": False, "error": "Bot not configured"}, status=400)
        try:
            data = json.loads(request.body)
            # Process webhook data here if needed
            logger.info(f"Telegram webhook: {data}")
            return JsonResponse({"ok": True})
        except json.JSONDecodeError:
            return JsonResponse({"ok": False}, status=400)
