import requests

class BaseNetworkService:
    """Parent Network Subsystem infrastructure."""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MusicDiscoveryMatrixPlatform/1.0 ( MamamiaMaria_1 )"
        })
        
    def _safe_get(self, direct_url):
        try:
            print(f"[OUTGOING API REQUEST] Forced Target String: {direct_url}")
            
            response = self.session.get(direct_url, timeout=10)
            print(f"[INCOMING RESPONSE STATUS] Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[LAST.FM ERROR CODES] Details: {response.text}")
                return {}

            return response.json()
            
        except requests.RequestException as e:
            print(f"Network subsystem dependency issue: {e}")
            return {}


