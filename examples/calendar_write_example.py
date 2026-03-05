import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('CALENDAR_API')
CALENDAR_ID = os.getenv('CALENDAR_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']

def add_event_in_two_hours():
    # 1. Authenticate and build service
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # 2. Calculate times
    # Get current time, add 2 hours for start, and make it 1 hour long
    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    end_time = start_time + datetime.timedelta(hours=1)

    # Convert to ISO format (Required by Google API)
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    # 3. Define the event body
    event_body = {
        'summary': 'API Test Event',
        'location': 'Virtual / Python Script',
        'description': 'This event was created automatically via the Google Calendar API.',
        'start': {
            'dateTime': start_iso,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    # 4. Execute the insert
    try:
        event = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
        print(f"✅ Success! Event created.")
        print(f"Link: {event.get('htmlLink')}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    add_event_in_two_hours()