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


@pytest.mark.integration
def test_view_events():
    get_calendar_service()
    result = view_events(datetime.datetime.now(), 10, True)


@pytest.mark.integration
def test_manage_event():
    get_calendar_service()
    start_time = datetime.datetime.now()

    result = add_event("Test Event", start_time, 2, "Test Location")

    edit_result = edit_event(result, title="Updated Event")

    delete_result = delete_event(result)

    assert "Event updated" in edit_result
    assert "Event deleted successfully" in delete_result
