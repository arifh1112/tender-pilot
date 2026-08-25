import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

def send_whatsapp_alert(recipient_phone: str, message_text: str):
    """
    Sends an outbound text alert via the Meta WhatsApp Cloud API.
    """
    if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID or WHATSAPP_API_TOKEN == "mock_token_for_now":
        print("⚠️ WhatsApp credentials not fully configured. Skipping actual network request.")
        print(f"Mock Notification to {recipient_phone}:\n{message_text}")
        return {"status": "skipped", "reason": "mock_credentials"}

    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200:
            print(f"✅ WhatsApp alert successfully sent to {recipient_phone}")
            return response_data
        else:
            print(f"❌ Failed to send WhatsApp alert: {response_data}")
            return response_data
    except Exception as e:
        print(f"❌ Network error while connecting to WhatsApp API: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Local dry-run test
    test_msg = "🚨 TenderPilot Alert: New tender detected (GEM/2026/B/9812450). Compliance document ready for review."
    send_whatsapp_alert("919876543210", test_msg)
