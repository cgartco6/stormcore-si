import os
from fastapi import FastAPI, Request, Response
from stormcore_si.tracking_telemetry import TargetTracker
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()

# Initialize our tracking database connections and gateway verifiers
tracker = TargetTracker(db_url=os.getenv("SUPABASE_URL"), db_key=os.getenv("SUPABASE_KEY"))
payment_handler = PaymentGatewayCoordinator()

@app.post("/api/webhook")
async def receive_payment_notification(request: Request):
    """
    Listens for live, incoming checkout completion confirmations.
    Processes and fractions income instantly upon validation.
    """
    # Ingest the raw form data sent by the gateway
    form_data = await request.form()
    payload = dict(form_data)
    
    # Extract the cryptographic signature sent by PayFast
    received_signature = payload.get("signature", "")
    
    if not received_signature:
        return Response(content="Missing Security Signature", status_code=400)
        
    # Verify that the notification came genuinely from PayFast and wasn't spoofed
    is_valid = payment_handler.verify_incoming_webhook_signature(payload, received_signature)
    
    if is_valid:
        payment_status = payload.get("payment_status")
        
        # Only process the split if the funds have actually cleared successfully
        if payment_status == "COMPLETE":
            gross_revenue = float(payload.get("amount_gross", 0.0))
            
            # Commit the transaction directly to our permanent tracking metrics ledger
            tracker.log_sale(item_price_zar=gross_revenue)
            
            print(f"[TREASURY] Transaction verified. R{gross_revenue:.2f} processed into internal split matrices.")
            return Response(content="OK", status_code=200)
            
        return Response(content="Notification Received but Payment Incomplete", status_code=200)
    else:
        print("[SECURITY BREACH] Received a payment notification with an invalid signature.")
        return Response(content="Invalid Cryptographic Signature", status_code=400)
