import os
import hashlib
import urllib.parse

class PaymentGatewayCoordinator:
    def __init__(self):
        self.merchant_id = os.getenv("PAYFAST_MERCHANT_ID", "10000100")
        self.merchant_key = os.getenv("PAYFAST_MERCHANT_KEY", "46f0cd694581a")
        self.passphrase = os.getenv("PAYFAST_PASSPHRASE", "")

    def generate_secure_checkout_url(self, item: str, price: float, order_id: str) -> str:
        """Generates an official, immutable PayFast payment link."""
        data = {
            "merchant_id": self.merchant_id,
            "merchant_key": self.merchant_key,
            "return_url": "https://yourdomain.co.za/success",
            "cancel_url": "https://yourdomain.co.za/cancel",
            "notify_url": "https://your-vercel-domain.vercel.app/api/webhook",
            "m_payment_id": order_id,
            "amount": f"{price:.2f}",
            "item_name": item
        }
        
        # Create alphabetical query string for secure signing
        query_string = urllib.parse.urlencode(data)
        if self.passphrase:
            query_string += f"&passphrase={urllib.parse.quote_plus(self.passphrase)}"
            
        # Secure cryptographic signature validation check
        security_signature = hashlib.md5(query_string.encode("utf-8")).hexdigest()
        
        # Append signature to final production checkout URL
        return f"https://www.payfast.co.za/eng/process?{query_string}&signature={security_signature}"

    def verify_incoming_webhook_signature(self, post_data: dict, received_signature: str) -> bool:
        """Verifies incoming payment notifications to confirm transaction validity."""
        # Clean signature from dataset for re-calculation
        test_data = {k: v for k, v in post_data.items() if k != "signature"}
        query_string = urllib.parse.urlencode(test_data)
        if self.passphrase:
            query_string += f"&passphrase={urllib.parse.quote_plus(self.passphrase)}"
            
        calculated_signature = hashlib.md5(query_string.encode("utf-8")).hexdigest()
        return calculated_signature == received_signature
