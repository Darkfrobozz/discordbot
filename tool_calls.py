from openai.types.chat import (
    ChatCompletionToolMessageParam,
    ChatCompletionMessageToolCallUnion,
    ChatCompletionMessageParam,
)
from typing import Iterable, Tuple
import datetime
import json

from calendar_tools import (
    add_event,
    delete_event,
    edit_event,
    view_events,
    set_calendar_timezone,
)
from tools import tools


def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny and 72°F."


def get_tools() -> list:
    return tools


def run_tools(
    tool_calls: list[ChatCompletionMessageToolCallUnion],
    context: Iterable[ChatCompletionMessageParam],
) -> Tuple[list[ChatCompletionMessageParam], bool]:
    context = list(context)

    any_tool_calls = False

    for tool_call in tool_calls:
        if tool_call.type != "function":
            continue
        func_name = tool_call.function.name

        print(tool_call.function.arguments)

        func_args = json.loads(tool_call.function.arguments)
        result = f"No tool was called using {func_name}"

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
        elif func_name == "set_calendar_timezone":
            result = set_calendar_timezone(**func_args)

        context.append(
            ChatCompletionToolMessageParam(
                role="tool", tool_call_id=tool_call.id, content=result
            )
        )
        any_tool_calls = True

    return (context, any_tool_calls)
