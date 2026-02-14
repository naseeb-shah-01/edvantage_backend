import httpx
from typing import Dict, Any

EMAIL_SERVER_URL = "https://email-sent-server-a.vercel.app/api/send-email"


def send_email_service(
    to: str,
    subject: str,
    template_name: str,
    data: Dict[str, Any],
):
    try:
        payload = {
            "to": to,
            "subject": subject,
            "templateName": template_name,
            "data": data,
        }

        response = httpx.post(EMAIL_SERVER_URL, json=payload, timeout=10.0)

        print(f"Email service response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Email sending failed: {str(e)}")