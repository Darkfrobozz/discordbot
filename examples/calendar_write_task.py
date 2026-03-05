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

def add_all_day_task(task_title):
    # 1. Authenticate
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # 2. Get today's date and tomorrow's date
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # 3. Define the event (Note we use 'date' instead of 'dateTime')
    event_body = {
        'summary': task_title,
        'description': 'This is an all-day task created via API.',
        'start': {
            'date': today.isoformat(), # Format: YYYY-MM-DD
        },
        'end': {
            'date': tomorrow.isoformat(), # All-day events end on the next day
        },
    }

    # 4. Execute
    try:
        event = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
        print(f"✅ Task created for {today}")
        print(f"Title: {event.get('summary')}")
        print(f"View here: {event.get('htmlLink')}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    add_all_day_task("Buy groceries and prep meals")