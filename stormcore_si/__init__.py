from .compliance_shield import ComplianceShield
from .tracking_telemetry import TargetTracker
from .platform_poster import PlatformPoster
from .payment_gateways import PaymentGatewayCoordinator

class StormcoreSIEngine:
    def __init__(self, db_url: str = None, db_key: str = None):
        """
        Unified operational engine framework wrapper.
        Can be initialized directly into past, present, or future repositories.
        """
        self.shield = ComplianceShield()
        self.tracker = TargetTracker(db_url=db_url, db_key=db_key)
        self.poster = PlatformPoster()
        self.payments = PaymentGatewayCoordinator()

    def execute_pure_pull_sequence(self, title: str, price: float, context_raw: str) -> dict:
        """Runs compliance checks, creates checkout mechanics, and logs metrics."""
        compliance_check = self.shield.verify_copy(context_raw)
        if not compliance_check["is_compliant"]:
            return {"status": "rejected", "reason": compliance_check["reason"]}
            
        checkout_link = self.payments.generate_secure_checkout_url(title, price, "AUTO_GEN_ID")
        
        return {
            "status": "approved",
            "target_item": title,
            "checkout_url": checkout_link,
            "broadcast_copy": f"{title} - Feature-complete specifications. Secure checkout link: {checkout_link}"
        }
