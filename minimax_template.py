import os
from openai import OpenAI
from dotenv import load_dotenv
from calendar_tools import get_calendar_service;

from typing import cast

load_dotenv()
get_calendar_service()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY"),
)

from tool_calls import get_tools, run_tools
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
    ChatCompletion
)

tools = get_tools()

messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": "Could you find the event at 15:00 2026 on the 12th of March in the calendar and delete it?"}
]

response : ChatCompletion | None = None
# Ralph loop:
for _ in range(10):
    # Create a new request:
    response = client.chat.completions.create(
        model="minimax/minimax-m2.5", messages=messages, tools=tools
    )

    # Get new tool_calls:
    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        break
    
    messages.append(cast(ChatCompletionMessageParam, response.choices[0].message))
    result = run_tools(tool_calls, messages)
    messages = result[0]
    tool_calling = result[1]

if response:
    print(response.choices[0].message.content) 
