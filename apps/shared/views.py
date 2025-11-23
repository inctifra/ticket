import json
from http import HTTPStatus

import requests
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from config.settings.base import env

API_KEY = env.str("IP_QUALITY_EMAIL_VERIFICATION_API_KEY")


class PrivacyView(TemplateView):
    template_name = "shared/pages/privacy.html"


# In-memory cache (module-level)
EMAIL_CHECK_CACHE = {}  # { email: { "valid": bool, "detail": str } }


def process_email(email: str) -> dict:
    url = f"https://ipqualityscore.com/api/json/email/{API_KEY}/{email}"
    params = {"fast": "false", "abuse_strictness": 0}
    response = requests.get(url, params=params, timeout=7)
    return response.json() if response.status_code == HTTPStatus.OK else None


@require_POST
@csrf_exempt
def validate_email_address(request: HttpRequest):
    try:
        email = json.loads(request.body)["email"].strip().lower()
    except (Exception, json.JSONDecodeError) as e:
        return JsonResponse({"detail": str(e)}, status=400, safe=False)

    # 🔍 1️⃣ Check cache first
    if email in EMAIL_CHECK_CACHE:
        return JsonResponse(
            EMAIL_CHECK_CACHE[email],
            safe=False,
            status=EMAIL_CHECK_CACHE[email].get("status"),
        )

    # 🌍 2️⃣ Call external API
    response = process_email(email)
    valid = bool(response.get("valid"))
    detail = response.get("reason") or (
        "Valid email" if valid else "Invalid email address"
    )

    # 💾 3️⃣ Store into cache
    EMAIL_CHECK_CACHE[email] = {
        "email": email,
        "valid": valid,
        "detail": detail,
        "status": 200 if valid else 400,
    }

    # 📤 4️⃣ Return result
    return JsonResponse(
        EMAIL_CHECK_CACHE[email], safe=False, status=200 if valid else 400
    )
