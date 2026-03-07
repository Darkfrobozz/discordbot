from openai.types.chat import ChatCompletionToolParam

weather_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "get_weather",
        "description": "Get the weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city name"}
            },
            "required": ["location"],
        },
    },
)

add_event_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "add_event",
        "description": "Creates an event in the Google calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the event"},
                "start_time": {
                    "type": "string",
                    "description": "The start time of the event in ISO 8601 format",
                },
                "duration": {
                    "type": "integer",
                    "description": "The duration of the event in hours",
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event",
                },
            },
            "required": ["title", "start_time", "duration", "location"],
        },
    },
)

delete_event_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "delete_event",
        "description": "Deletes an event from the Google calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to delete",
                },
            },
            "required": ["event_id"],
        },
    },
)

edit_event_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "edit_event",
        "description": "Edits an event in the Google calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to edit",
                },
                "title": {
                    "type": "string",
                    "description": "The new title for the event",
                },
                "description": {
                    "type": "string",
                    "description": "The new description for the event",
                },
                "location": {
                    "type": "string",
                    "description": "The new location for the event",
                },
            },
            "required": ["event_id"],
        },
    },
)

view_events_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "view_events",
        "description": "Views all events in the Google calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "minimumTime": {
                    "type": "string",
                    "description": "The minimum time for events in ISO 8601 format",
                },
                "maxResults": {
                    "type": "integer",
                    "description": "The maximum number of events to return",
                },
                "singleEvents": {
                    "type": "boolean",
                    "description": "Whether to expand recurring events",
                },
            },
            "required": ["minimumTime", "maxResults", "singleEvents"],
        },
    },
)

set_calendar_timezone_tool = ChatCompletionToolParam(
    type="function",
    function={
        "name": "set_calendar_timezone",
        "description": "Sets the timezone for all future calendar operations",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone_str": {
                    "type": "string",
                    "description": "The timezone to set (e.g., 'Europe/Stockholm', 'UTC', 'America/New_York')",
                },
            },
            "required": ["timezone_str"],
        },
    },
)

tools = [
    weather_tool,
    add_event_tool,
    delete_event_tool,
    edit_event_tool,
    view_events_tool,
    set_calendar_timezone_tool,
]
