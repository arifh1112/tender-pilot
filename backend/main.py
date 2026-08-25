from fastapi import FastAPI
from backend.webhook.whatsapp import router as whatsapp_router

app = FastAPI(
    title="TenderPilot Core API",
    description="AI-powered bid intelligence copilot for GeM and CPPP public procurement.",
    version="1.0.0"
)

# Include routers
app.include_router(whatsapp_router)

@app.get("/")
def health_check():
    return {
        "status": "TenderPilot Engine Online",
        "stack": "FastAPI + Playwright + DeepSeek-R1",
        "infrastructure_cost": "~₹3,500/month target active"
    }
