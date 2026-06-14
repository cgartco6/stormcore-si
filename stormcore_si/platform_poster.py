import os
import requests

class PlatformPoster:
    def __init__(self):
        # Tokens securely fetched from your dashboard's environment variables
        self.meta_page_token = os.getenv("META_PAGE_ACCESS_TOKEN", "")
        self.meta_page_id = os.getenv("META_PAGE_ID", "")
        self.tiktok_open_api_url = "https://open.tiktokapis.com/v2/post/publish/"

    def publish_organic_broadcast(self, clean_copy: str, asset_url: str) -> dict:
        """
        Dispatches your compliant text and synthetic media link natively.
        Bypasses traditional ad tools to optimize for organic reach.
        """
        if not self.meta_page_token or not self.meta_page_id:
            # Fallback simulator for safe sandbox testing
            print("[POSTER] Simulation Mode: Environment keys missing. Logging payload output:")
            print(f" -> Text: {clean_copy}\n -> Asset Source: {asset_url}")
            return {"status": "simulated_success", "platform": "meta_sandbox"}

        # Production Meta API execution hook
        meta_url = f"https://graph.facebook.com/v18.0/{self.meta_page_id}/photos"
        payload = {
            "caption": clean_copy,
            "url": asset_url,
            "access_token": self.meta_page_token
        }
        
        try:
            res = requests.post(meta_url, data=payload, timeout=10)
            if res.status_code == 200:
                return {"status": "deployed", "id": res.json().get("id")}
            return {"status": "failed", "error": res.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}
