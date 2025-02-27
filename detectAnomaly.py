from getToken import APIClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import sys
import os

## Pass API key from terminal or environmental variable
API_KEY = os.getenv("API_KEY")
AUTH_URL = "https://api.verkada.com/token"
BASE_URL = "https://api.verkada.com/events/v1/"

## Manage time
dt = datetime.now(timezone.utc)
five_minutes_past = dt - timedelta(minutes=5)
then = int(five_minutes_past.timestamp())
present = dt.timestamp()

## Connect to API
client = APIClient(API_KEY, AUTH_URL, BASE_URL)
endpoint = f"access?start_time={then}&page_size=100&event_type=door_keycard_entered_rejected"
response = client.make_request(endpoint)
eventList = response['events']
deviceList = defaultdict(int)

## Process events
for event in eventList:
    deviceList[event["device_id"]] += 1

for device in deviceList:
    if deviceList[device] > 4:
            print(f"Too many auth failures on {device}")

