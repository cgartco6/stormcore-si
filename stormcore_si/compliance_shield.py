class ComplianceShield:
    def __init__(self):
        # Strict core boundaries matching purely objective pull marketing strategies
        self.banned_triggers = [
            "hurry", "limited", "special", "offer", "buy now", 
            "today only", "click here", "dm me", "act fast"
        ]

    def verify_copy(self, raw_description: str) -> dict:
        """Parses advertising copy blocks for compliance, stripping out artificial urgency patterns."""
        clean_text = raw_description.lower()
        
        # Scan copy for manipulative patterns or banned trigger keywords
        for trigger in self.banned_triggers:
            if trigger in clean_text:
                return {
                    "is_compliant": False,
                    "reason": f"Compliance anomaly: Outlawed high-pressure sales element detected -> '{trigger}'"
                }
        
        # Algorithmic text formatting audit: flags hyperactive exclamation marks or emoji spam
        if clean_text.count("!") > 1 or clean_text.count("🔥") > 0:
            return {
                "is_compliant": False,
                "reason": "Compliance anomaly: Robotic formatting spam detected. Convert text back to human-like flow traits."
            }
            
        return {"is_compliant": True, "reason": "Copy structures verified safe for programmatic publication."}
