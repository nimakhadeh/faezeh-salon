"""
Zarinpal Payment Gateway Integration
"""

import requests
import json
from django.conf import settings


class ZarinpalPayment:
    def __init__(self):
        config = settings.ZARINPAL
        self.merchant_id = config.get("MERCHANT_ID", "")
        self.sandbox = config.get("SANDBOX", True)
        self.callback_url = config.get("CALLBACK_URL", "")

        if self.sandbox:
            self.api_url = "https://sandbox.zarinpal.com/pg/v4/payment"
            self.payment_url = "https://sandbox.zarinpal.com/pg/StartPay/"
        else:
            self.api_url = "https://api.zarinpal.com/pg/v4/payment"
            self.payment_url = "https://www.zarinpal.com/pg/StartPay/"

    def request_payment(self, amount, description, callback_url=None, metadata=None):
        """
        Request a payment from Zarinpal.
        amount: in Tomans
        """
        if not self.merchant_id:
            return {"success": False, "error": "Zarinpal merchant ID is not configured."}

        url = f"{self.api_url}/request.json"
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "description": description,
            "callback_url": callback_url or self.callback_url,
            "metadata": metadata or {},
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()

            if response.status_code == 200:
                result = data.get("data", {})
                errors = data.get("errors", [])

                if result.get("code") == 100:
                    authority = result.get("authority")
                    return {
                        "success": True,
                        "authority": authority,
                        "payment_url": f"{self.payment_url}{authority}",
                    }
                elif errors:
                    return {
                        "success": False,
                        "error": f"Zarinpal Error {errors[0].get('code')}: {errors[0].get('message', 'Unknown error')}",
                    }
                else:
                    return {"success": False, "error": f"Unexpected response: {data}"}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}

    def verify_payment(self, authority, amount):
        """
        Verify a payment with Zarinpal.
        """
        if not self.merchant_id:
            return {"success": False, "error": "Zarinpal merchant ID is not configured."}

        url = f"{self.api_url}/verify.json"
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()

            if response.status_code == 200:
                result = data.get("data", {})
                errors = data.get("errors", [])

                code = result.get("code")
                if code in [100, 101]:
                    return {
                        "success": True,
                        "ref_id": str(result.get("ref_id", "")),
                        "card_pan": result.get("card_pan", ""),
                        "code": code,
                        "message": "پرداخت با موفقیت تأیید شد." if code == 100 else "پرداخت قبلاً تأیید شده است.",
                    }
                elif errors:
                    return {
                        "success": False,
                        "error": f"Zarinpal Error {errors[0].get('code')}: {errors[0].get('message', 'Verification failed')}",
                    }
                else:
                    return {"success": False, "error": f"Payment failed with code {code}."}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}

    def get_payment_url(self, authority):
        return f"{self.payment_url}{authority}"
