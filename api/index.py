import os
import sys

# Force the Python runtime execution environment to recognize the root repository directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Core engine imports
from stormcore_si import ComplianceShield, TargetTracker
from stormcore_si.platform_poster import PlatformPoster
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shield = ComplianceShield()
tracker = TargetTracker(db_url=os.getenv("SUPABASE_URL"), db_key=os.getenv("SUPABASE_KEY"))
poster = PlatformPoster()
payment = PaymentGatewayCoordinator()

# ==============================================================================
# NATIVE FRONTEND ROUTING BLOCKS (No vercel.json rewrites required)
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard_home():
    """Serves your mobile web control panel directly at the main domain root."""
    try:
        with open("public/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception:
        return HTMLResponse(content="<h1>Stormcore-SI UI File Missing in /public Folder</h1>", status_code=404)

@app.get("/manifest.json")
async def serve_manifest():
    """Natively serves the PWA mobile install configuration file."""
    try:
        with open("public/manifest.json", "r", encoding="utf-8") as f:
            return JSONResponse(content=json.load(f))
    except Exception:
        # Hardcoded raw fallback to ensure the PWA features never brick
        return JSONResponse({
            "name": "Stormcore-SI Mobile Control",
            "short_name": "Stormcore",
            "start_url": "/",
            "display": "standalone",
            "orientation": "portrait",
            "background_color": "#020617",
            "theme_color": "#4f46e5"
        })

@app.get("/sw.js")
async def serve_service_worker():
    """Serves the background service worker caching layer."""
    try:
        with open("public/sw.js", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except Exception:
        return Response(content="", media_type="application/javascript")

# ==============================================================================
# EXISTING BACKEND OPERATION ENDPOINTS
# ==============================================================================

@app.get("/api/metrics")
async def get_metrics_endpoint():
    metrics = tracker.read_metrics()
    return JSONResponse(metrics)

@app.post("/api/launch")
async def mobile_launch_endpoint(
    name: str = Form(...), 
    price: float = Form(...), 
    description: str = Form(...)
):
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
