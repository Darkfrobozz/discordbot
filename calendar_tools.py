from pydantic import BaseModel, Field
from typing import Optional

import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


class EventTime(BaseModel):
    # Use 'date' for All-Day tasks, 'dateTime' for timed events
    date: Optional[str] = None
    dateTime: Optional[str] = None
    timeZone: Optional[str] = "UTC"


class GoogleCalendarTask(BaseModel):
    id: Optional[str] = None
    summary: str
    description: Optional[str] = ""
    start: EventTime
    end: EventTime
    colorId: Optional[str] = None
    htmlLink: Optional[str] = None

    class Config:
        # This allows the model to ignore extra fields Google might send
        extra = "ignore"


# Load environment variables
load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("CALENDAR_API")
CALENDAR_ID = os.getenv("CALENDAR_ID")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    if not SERVICE_ACCOUNT_FILE or not CALENDAR_ID:
        raise ValueError("Missing CALENDAR_API or CALENDAR_ID in .env file")

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    return build("calendar", "v3", credentials=creds)


def add_event(
    title: str, start_time: datetime.datetime, duration: int, location: str
) -> str:
    """
    This function creates an event in the google calendar,
    it returns the id of the added event or a message saying that adding failed
    """
    service = get_calendar_service()

    end_time = start_time + datetime.timedelta(hours=duration)

    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    event_body = {
        "summary": title,
        "location": location,
        "description": "",
        "start": {
            "dateTime": start_iso,
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_iso,
            "timeZone": "UTC",
        },
        "reminders": {
            "useDefault": True,
        },
    }

    try:
        event = (
            service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
        )
        return event.get("id")
    except Exception as e:
        return f"Failed to create event: {str(e)}"


def view_events(
    minimumTime: datetime.datetime, maxResults: int, singleEvents: bool
) -> list[GoogleCalendarTask]:
    """
    This function views all the events in the calendar
    """
    service = get_calendar_service()

    events_result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=minimumTime.isoformat() + "Z",
            maxResults=maxResults,
            singleEvents=singleEvents,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    return [GoogleCalendarTask(**event) for event in events]


def edit_event(
    event_id: str,
    title: str | None = None,
    description: str | None = None,
    location: str | None = None,
) -> str:
    """
    This function should return the result from the API from editting the task.
    """
    service = get_calendar_service()

    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    if title is not None:
        event["summary"] = title
    if description is not None:
        event["description"] = description
    if location is not None:
        event["location"] = location

    updated_event = (
        service.events()
        .update(calendarId=CALENDAR_ID, eventId=event_id, body=event)
        .execute()
    )
    return f"Event updated: {updated_event.get('htmlLink')}"


def delete_event(event_id: str) -> str:
    """
    Deletes an event
    """
    service = get_calendar_service()
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
    return f"Event deleted successfully"
