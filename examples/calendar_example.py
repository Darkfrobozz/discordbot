import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load variables from .env
load_dotenv()

# Fetch variables
SERVICE_ACCOUNT_FILE = os.getenv('CALENDAR_API')
CALENDAR_ID = os.getenv('CALENDAR_ID')

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    if not SERVICE_ACCOUNT_FILE or not CALENDAR_ID:
        raise ValueError("Missing CALENDAR_API or CALENDAR_ID in .env file")

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    return build('calendar', 'v3', credentials=creds)

def list_upcoming_events():
    service = get_calendar_service()
    
    # Get current time in UTC
    now = datetime.datetime.utcnow().isoformat() + 'Z' 

    print(f"Checking events for Calendar: {CALENDAR_ID}...")

    events_result = service.events().list(
        calendarId=CALENDAR_ID, 
        timeMin=now,
        maxResults=5, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Found: {event['summary']} at {start}")

if __name__ == '__main__':
    list_upcoming_events()