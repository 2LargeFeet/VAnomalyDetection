from getToken import APIClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import requests
import sys
import os

## Pass API key from terminal or environmental variable
API_KEY = os.getenv("API_KEY")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")
AUTH_URL = "https://api.verkada.com/token"
BASE_URL = "https://api.verkada.com/events/v1/"

## Manage notifications
def sendTeamsNotification(notification):
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Large",
                            "weight": "Bolder",
                            "text": "New Access Alert"
                        },
                        {
                            "type": "TextBlock",
                            "text": notification,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }
    response = requests.post(TEAMS_WEBHOOK, json=payload)

## Manage time
dt = datetime.now(timezone.utc)
five_minutes_past = dt - timedelta(minutes=5)
then = int(five_minutes_past.timestamp())
present = dt.timestamp()

## Connect to API
client = APIClient(API_KEY, AUTH_URL, BASE_URL)
eventEndpoint = f"access?start_time={then}&page_size=100&event_type=door_keycard_entered_rejected"
eventResponse = client.make_request(eventEndpoint)
eventList = eventResponse['events']
deviceList = defaultdict(int)

## Process events
for event in eventList:
    deviceList[event["device_id"]] += 1

for device in deviceList:
    if deviceList[device] > 4:
        notification = f"Too many auth failures on {device}"
        sendTeamsNotification(notification)
