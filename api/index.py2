import os
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import your underlying core modules
from stormcore_si import ComplianceShield, TargetTracker
from stormcore_si.platform_poster import PlatformPoster
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()

# Enable cross-origin requests so your mobile dashboard can talk to the backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules cleanly
shield = ComplianceShield()
tracker = TargetTracker(db_url=os.getenv("SUPABASE_URL"), db_key=os.getenv("SUPABASE_KEY"))
poster = PlatformPoster()
payment = PaymentGatewayCoordinator()

@app.get("/api/metrics")
async def get_metrics_endpoint():
    """Fetches real-time telemetry metrics directly from the data ledger."""
    metrics = tracker.read_metrics()
    return JSONResponse(metrics)

@app.post("/api/launch")
async def mobile_launch_endpoint(
    name: str = Form(...), 
    price: float = Form(...), 
    description: str = Form(...)
):
    """Processes organic pure-pull marketing copy validation and payment link creation."""
    check = shield.verify_copy(description)
    if not check["is_compliant"]:
        return JSONResponse({"status": "rejected", "reason": check["reason"]}, status_code=400)
        
    checkout_url = payment.generate_secure_checkout_url(name, price, "ORDER_1001")
    ad_copy = f"{name} - Available natively. Secure Checkout: {checkout_url}"
    post_result = poster.publish_organic_broadcast(ad_copy, "https://images.unsplash.com/photo-1543083505-590d4eeef7c3")
    
    return JSONResponse({
        "status": "approved",
        "message": f"Successfully launched! Published to platform APIs. Payment processing active.",
        "checkout_url": checkout_url
    })

@app.post("/api/webhook")
async def receive_payment_notification(request: Request):
    """Listens for live checkout completions from your payment provider."""
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
