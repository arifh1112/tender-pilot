from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

@router.post("/webhook/whatsapp/alert")
async def send_whatsapp_alert(phone_number: str, bid_id: str, summary_text: str):
    """
    Sends automated WhatsApp alerts to contractors with 1-page qualification summaries.
    """
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        raise HTTPException(
            status_code=500, 
            detail="WhatsApp API credentials not configured in environment variables."
        )
        
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "tender_alert_summary",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": bid_id},
                        {"type": "text", "text": summary_text[:1000]}
                    ]
                }
            ]
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=response.text)
    
    return {"status": "success", "message": "WhatsApp alert sent successfully"}
