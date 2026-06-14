import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from stormcore_si import ComplianceShield, TargetTracker
from stormcore_si.platform_poster import PlatformPoster
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()
shield = ComplianceShield()
tracker = TargetTracker(db_url=os.getenv("SUPABASE_URL"), db_key=os.getenv("SUPABASE_KEY"))
poster = PlatformPoster()
payment = PaymentGatewayCoordinator()

@app.post("/api/launch")
async def mobile_launch_endpoint(
    name: str = Form(...), 
    price: float = Form(...), 
    description: str = Form(...)
):
    # Run compliance verification
    check = shield.verify_copy(description)
    if not check["is_compliant"]:
        return JSONResponse({"status": "rejected", "reason": check["reason"]}, status_code=400)
        
    # Generate the payment link
    checkout_url = payment.generate_secure_checkout_url(name, price, "ORDER_1001")
    
    # Format and publish the creative copy
    ad_copy = f"{name} - Available natively. Secure Checkout: {checkout_url}"
    post_result = poster.publish_organic_broadcast(ad_copy, "https://images.unsplash.com/photo-1543083505-590d4eeef7c3")
    
    return JSONResponse({
        "status": "approved",
        "message": f"Successfully launched! Published to platform APIs. Payment processing active.",
        "checkout_url": checkout_url
    })
