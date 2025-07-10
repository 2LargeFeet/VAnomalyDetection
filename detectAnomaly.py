from getToken import APIClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import json
import requests
import sys
import os
import time

## Pass API key from terminal or environmental variable
API_KEY = os.getenv("API_KEY")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")
AUTH_URL = "https://api.verkada.com/token"
EVENTS_URL = "https://api.verkada.com/events/v1/"
USERS_URL = "https://api.verkada.com/access/v1/access_users/user"
DOOR_URL = "https://api.verkada.com/access/v1/doors"

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
    
## Get Door Name
def get_door_name(device, headers):
    door_URL_w_Endpoint = f"{DOOR_URL}?door_ids={device}"
    response = requests.get(door_URL_w_Endpoint, headers=headers)
    responseJson = response.json()
    doors = responseJson['doors']
    for door in doors:
        if door["door_id"] == device:
            doorName = door["name"]
    return doorName

def detect_excessive_denies():
    dt = datetime.now(timezone.utc)
    five_minutes_past = dt - timedelta(minutes=5)
    then = int(five_minutes_past.timestamp())
    present = dt.timestamp()
    client = APIClient(api_key=API_KEY, auth_url=AUTH_URL)
    token = client.get_api_token()
    url = f"{EVENTS_URL}/access?start_time={then}&page_size=100&event_type=door_keycard_entered_rejected"
    headers = { 
        "x-verkada-auth": token,
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    responseJson = response.json()
    eventList = responseJson['events']
    deviceList = defaultdict(int)
    for event in eventList:
        deviceList[event["device_id"]] += 1
    for device in deviceList:
        if deviceList[device] > 4:
            doorName = get_door_name(device, headers)
            notification = f"Too many auth failures on {doorName}"
            sendTeamsNotification(notification)

def application():
    while True:
        detect_excessive_denies()
        time.sleep(300)
        
if __name__ == "__main__":
    application()