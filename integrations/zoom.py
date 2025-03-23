import json
import uuid
import requests
from datetime import datetime, timedelta
import pytz
import os

def get_zoom_access_token():
    """
    Obtains a Zoom access token using server-to-server OAuth.
    Your credentials JSON file should have the keys:
      - client_id
      - client_secret
      - account_id
      - user_id (optional; if not provided, "me" will be used)
    """
    # with open(credentials_file) as f:
    #     creds = json.load(f)
        
    account_id = 'Cpsg32mDQJ6C8utKqR7ABg'
    client_id = 'G6Hu0sCQTTY3S50wRTKdg'
    client_secret = 'B9CB0BS8UAUk1s39gQhUyKyiEThWIhC8'

    # Construct token URL according to Zoom's server-to-server OAuth guide
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={account_id}"
    # Send a POST request with HTTP basic authentication (client_id and client_secret)
    response = requests.post(url, auth=(client_id, client_secret))
    response.raise_for_status()  # Raise an exception if the request failed
    token = response.json()["access_token"]
    return token

def create_zoom_meeting(credentials_file, topic, agenda, start_time, duration, time_zone, max_participants):
    """
    Creates a Zoom scheduled meeting using a server-to-server OAuth app.
    
    Note:
      - 'start_time' should be in ISO 8601 format.
      - Zoom does not support 'max_participants' in the creation payload; it is determined by your Zoom plan.
    """
    token = get_zoom_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Read credentials to get the userId. If not provided, default to "me"
    # with open(credentials_file) as f:
    #     creds = json.load(f)
    # user_id = creds.get("user_id", "me")
    
    url = f"https://api.zoom.us/v2/users/me/meetings"
    
    payload = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time,  # ISO 8601 format
        "duration": duration,      # Duration in minutes
        "timezone": time_zone,
        "agenda": agenda,
        "settings": {
            "approval_type": 0,              # Automatically approve participants
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "waiting_room": True,
            "meeting_authentication": False,
            "registrants_email_notification": False,
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    meeting = response.json()
    return meeting

def update_zoom_meeting(credentials_file, meeting_id, topic=None, agenda=None, start_time=None, duration=None, time_zone=None):
    """
    Updates a Zoom meeting using a server-to-server OAuth app.
    Only fields that are provided will be updated.
    """
    token = get_zoom_access_token(credentials_file)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    payload = {}
    
    if topic:
        payload["topic"] = topic
    if agenda:
        payload["agenda"] = agenda
    if start_time:
        payload["start_time"] = start_time
    if duration:
        payload["duration"] = duration
    if time_zone:
        payload["timezone"] = time_zone

    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    # Zoom returns an empty response body on a successful update so we return the status code.
    return response.status_code

# Example usage:
if __name__ == "__main__":
    credentials_file = 'zoom_credentials.json'  # Replace with your credentials file containing Zoom app details
    
    # Define meeting start time in London time zone (tomorrow) and duration in minutes
    london_tz = pytz.timezone('Europe/London')
    start_time_dt = (datetime.now(london_tz) + timedelta(days=1)).replace(microsecond=0)
    start_time = start_time_dt.isoformat()
    duration = 100  # Meeting duration in minutes
    
    print(f"Creating Zoom meeting scheduled to start at {start_time} for {duration} minutes")
    
    zoom_meeting = create_zoom_meeting(
        credentials_file=credentials_file,
        topic='Bot-Created Zoom Meeting',
        agenda='A meeting created by a bot.',
        start_time=start_time,
        duration=duration,
        time_zone='Europe/London',
        max_participants=10,  # For reference; actual participant limits are set by your Zoom plan.
    )
    
    print(f"Zoom meeting join link: {zoom_meeting.get('join_url')}")
    print(f"Meeting ID: {zoom_meeting.get('id')}")
    print(f"Meeting created at: {zoom_meeting.get('created_at')}")
    
    # Example of updating the meeting (e.g., changing the topic/agenda)
    # meeting_id = zoom_meeting.get('id')
    # update_status = update_zoom_meeting(
    #     credentials_file=credentials_file,
    #     meeting_id=meeting_id,
    #     topic="Updated Bot-Created Zoom Meeting",
    #     agenda="Updated agenda for the meeting."
    # )
    # print(f"Update status code: {update_status}")