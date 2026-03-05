from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionToolParam,
    ChatCompletionMessageToolCallUnion,
    ChatCompletionMessageParam,
)
from typing import Iterable

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

# Then just put it in your list
tools: list[ChatCompletionToolParam] = [weather_tool]


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
        result = ""

        if func_name == "get_weather":
            result = get_weather(**func_args)

        context.append(
            ChatCompletionToolMessageParam(
                role="tool", tool_call_id=tool_call.id, content=result
            )
        )

    return context
