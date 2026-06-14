import os
import json
import requests

class TargetTracker:
    def __init__(self, db_url: str = None, db_key: str = None, local_fallback_path: str = "data/metrics_cache.json"):
        """Handles metric orchestration across both serverless databases and local system execution paths."""
        self.db_url = db_url
        self.db_key = db_key
        self.local_path = local_fallback_path
        
        if not self.db_url:
            os.makedirs(os.path.dirname(self.local_path) or '.', exist_ok=True)

    def read_metrics(self) -> dict:
        """Pulls transaction statistics from the cloud database, falling back to local files if offline."""
        if self.db_url and self.db_key:
            headers = {"apikey": self.db_key, "Authorization": f"Bearer {self.db_key}"}
            try:
                res = requests.get(f"{self.db_url}/rest/v1/stormcore_telemetry?order=id.desc&limit=1", headers=headers, timeout=4)
                if res.status_code == 200 and len(res.json()) > 0:
                    return res.json()[0]
            except Exception:
                pass # Fail silently and read local system state fallback
                
        if os.path.exists(self.local_path):
            with open(self.local_path, "r") as f:
                return json.load(f)
        return {"growth_count": 0, "revenue_total": 0.0, "compliance_runs": 0}

    def log_sale(self, item_price_zar: float):
        """Saves transaction amounts and updates execution values."""
        metrics = self.read_metrics()
        metrics["growth_count"] += 1
        metrics["revenue_total"] += item_price_zar
        metrics["compliance_runs"] = metrics.get("compliance_runs", 0) + 1
        
        if self.db_url and self.db_key:
            headers = {
                "apikey": self.db_key, 
                "Authorization": f"Bearer {self.db_key}", 
                "Content-Type": "application/json"
            }
            try:
                requests.post(f"{self.db_url}/rest/v1/stormcore_telemetry", headers=headers, json=metrics, timeout=4)
                return
            except Exception:
                pass
                
        with open(self.local_path, "w") as f:
            json.dump(metrics, f, indent=4)
