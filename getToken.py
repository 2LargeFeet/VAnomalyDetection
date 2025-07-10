import time
import requests

class APIClient:
    def __init__(self, api_key, auth_url):
        self.api_key = api_key
        self.auth_url = auth_url
        self.api_token = None
        self.token_expiry = 0

    def _is_token_valid(self):
        return self.api_token and time.time() < self.token_expiry

    def _refresh_token(self):
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }
        response = requests.post(self.auth_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.api_token = data.get("token")
            self.token_expiry = time.time() + 1800
        else:
            raise Exception(f"Failed to obtain API token: {response.text}")

    def get_api_token(self):
        if not self._is_token_valid():
            self._refresh_token()
        return self.api_token
