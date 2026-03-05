import pytest
import datetime
from unittest.mock import patch, MagicMock

from calendar_tools import (
    get_calendar_service,
    add_event,
    view_events,
    edit_event,
    delete_event,
    GoogleCalendarTask,
    EventTime,
)


def test_view_events():
    mock_service = MagicMock()
    with patch.object(get_calendar_service, "__call__", return_value=mock_service):
        mock_service.events().list().execute.return_value = {
            "items": [
                {
                    "id": "event1",
                    "summary": "Test Event",
                    "description": "Test description",
                    "start": {
                        "dateTime": "2024-01-01T10:00:00+00:00",
                        "timeZone": "UTC",
                    },
                    "end": {"dateTime": "2024-01-01T12:00:00+00:00", "timeZone": "UTC"},
                }
            ]
        }

        result = view_events(datetime.datetime.now(), 10, True)

        mock_service.events().list.assert_called_once()


def test_manage_event():
    mock_service = MagicMock()
    with patch.object(get_calendar_service, "__call__", return_value=mock_service):
        mock_service.events().insert().execute.return_value = {
            "id": "test123",
            "htmlLink": "https://calendar.google.com/event?eid=test123",
            "summary": "Test Event",
            "description": "",
            "location": "Test Location",
        }
        mock_service.events().update().execute.return_value = {
            "htmlLink": "https://calendar.google.com/event?eid=test123"
        }

        start_time = datetime.datetime.now()

        result = add_event("Test Event", start_time, 2, "Test Location")

        edit_result = edit_event(result, title="Updated Event")

        delete_result = delete_event(result)

        assert "Event updated" in edit_result
        assert "Event deleted successfully" in delete_result
        mock_service.events().insert.assert_called_once()
