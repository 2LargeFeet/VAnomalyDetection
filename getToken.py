import time
import requests

class APIClient:
    def __init__(self, api_key, auth_url, base_url):
        self.api_key = api_key
        self.auth_url = auth_url
        self.base_url = base_url
        self.api_token = None
        self.token_expiry = 0
    def get_api_token(self):
        """Fetch a new API token if the current one is expired."""
        if self.api_token and time.time() < self.token_expiry:
            return self.api_token
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }
        response = requests.post(self.auth_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.api_token = data.get("token")
            self.token_expiry = time.time() + 1800
            return self.api_token
        else:
            raise Exception(f"Failed to obtain API token: {response.text}")

    def make_request(self, endpoint="access", method="GET", data=None, params=None):
        """Make an authenticated API request."""
        token = self.get_api_token()
        headers = { 
            "x-verkada-auth": token,
            "accept": "application/json"
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, json=data, params=params)
        if response.status_code == 401:
            self.api_token = None
            return self.make_request(endpoint, method, data, params)
        return response.json()
