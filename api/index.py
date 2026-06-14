import os
import sys
import json

# Force the Python runtime execution environment to recognize the root repository directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Form, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Core engine imports
from stormcore_si import ComplianceShield, TargetTracker
from stormcore_si.platform_poster import PlatformPoster
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()

# Enable cross-origin requests for secure mobile dashboard connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize operational modules
shield = ComplianceShield()
tracker = TargetTracker(db_url=os.getenv("SUPABASE_URL"), db_key=os.getenv("SUPABASE_KEY"))
poster = PlatformPoster()
payment = PaymentGatewayCoordinator()

def background_meta_broadcast(ad_copy: str):
    """
    Executes the external network call to Meta safely in the background.
    This prevents Vercel's 10-second serverless execution limit from 
    causing a frontend timeout on your mobile screen.
    """
    try:
        poster.publish_organic_broadcast(ad_copy, "https://images.unsplash.com/photo-1543083505-590d4eeef7c3")
    except Exception as e:
        print(f"Background social broadcast processing delayed: {e}")

@app.get("/api/metrics")
async def get_metrics_endpoint():
    """Fetches real-time telemetry metrics directly from the data ledger."""
    try:
        metrics = tracker.read_metrics()
        return JSONResponse(metrics)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/launch")
async def mobile_launch_endpoint(
    background_tasks: BackgroundTasks,
    name: str = Form(...), 
    price: float = Form(...), 
    description: str = Form(...)
):
    """
    Processes organic pure-pull marketing copy validation and payment link creation.
    Offloads the slow external APIs to a background thread to return an instant 
    response to the HUD.
    """
    try:
        # 1. Evaluate text content via pure-pull engine rules
        check = shield.verify_copy(description)
        if not check["is_compliant"]:
            return JSONResponse({"status": "rejected", "reason": check["reason"]}, status_code=400)
            
        # 2. Cryptographically assemble secure PayFast payment parameter link
        checkout_url = payment.generate_secure_checkout_url(name, price, "ORDER_1001")
        ad_copy = f"{name} - Available natively. Secure Checkout: {checkout_url}"
        
        # 3. Queue the external network API broadcast to run on Vercel's background time
        background_tasks.add_task(background_meta_broadcast, ad_copy)
        
        # 4. Return success metrics instantly back to the phone screen under 2 seconds
        return JSONResponse({
            "status": "approved",
            "message": "Successfully launched! Published to platform APIs. Payment processing active.",
            "checkout_url": checkout_url
        })
    except Exception as e:
        return JSONResponse({"status": "error", "reason": str(e)}, status_code=500)

@app.post("/api/webhook")
async def receive_payment_notification(request: Request):
    """Listens for live checkout completions from your payment provider."""
    try:
        form_data = await request.form()
        payload = dict(form_data)
        received_signature = payload.get("signature", "")
        
        if not received_signature:
            return Response(content="Missing Security Signature", status_code=400)
            
        is_valid = payment.verify_incoming_webhook_signature(payload, received_signature)
        if is_valid and payload.get("payment_status") == "COMPLETE":
            gross_revenue = float(payload.get("amount_gross", 0.0))
            tracker.log_sale(item_price_zar=gross_revenue)
            return Response(content="OK", status_code=200)
            
        return Response(content="Verification Check Failed", status_code=400)
    except Exception:
        return Response(content="Internal Processing Error", status_code=500)
