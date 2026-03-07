from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionToolParam,
    ChatCompletionMessageToolCallUnion,
    ChatCompletionMessageParam,
)
from typing import Iterable
import datetime

from calendar_tools import (
    get_calendar_service,
    add_event,
    delete_event,
    edit_event,
    view_events,
)

# Define the tool as a typed object
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


# Then just put it in your list
# TODO add the new tools:
tools: list[ChatCompletionToolParam] = [
    weather_tool,
    add_event_tool,
    delete_event_tool,
    edit_event_tool,
    view_events_tool,
]


# Tools:
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny and 72°F."


# Endpoint:


def get_tools() -> list[ChatCompletionToolParam]:
    return tools


def run_tools(
    tool_calls: list[ChatCompletionMessageToolCallUnion],
    context: Iterable[ChatCompletionMessageParam],
) -> list[ChatCompletionMessageParam]:
    context = list(context)

    for tool_call in tool_calls:
        if tool_call.type != "function":
            continue
        func_name = tool_call.function.name
        func_args = eval(tool_call.function.arguments)
        result = f"No tool was called using {func_name}"

        # TODO Replace the following with a switch for each available function, default does not do anything
        if func_name == "get_weather":
            result = get_weather(**func_args)
        elif func_name == "add_event":
            func_args["start_time"] = datetime.datetime.fromisoformat(
                func_args["start_time"]
            )
            result = add_event(**func_args)
        elif func_name == "delete_event":
            result = delete_event(**func_args)
        elif func_name == "edit_event":
            result = edit_event(**func_args)
        elif func_name == "view_events":
            func_args["minimumTime"] = datetime.datetime.fromisoformat(
                func_args["minimumTime"]
            )
            events = view_events(**func_args)
            result = str([event.model_dump() for event in events])

        context.append(
            ChatCompletionToolMessageParam(
                role="tool", tool_call_id=tool_call.id, content=result
            )
        )

    return context
