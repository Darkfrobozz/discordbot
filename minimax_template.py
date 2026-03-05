import os
from openai import OpenAI
from dotenv import load_dotenv

from typing import cast

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY"),
)

from tool_calls import get_tools, run_tools
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)

tools = get_tools()

messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": "What's the weather in Tokyo?"}
]

response = client.chat.completions.create(
    model="minimax/minimax-m2.5", messages=messages, tools=tools
)

tool_calls = response.choices[0].message.tool_calls

if tool_calls and tool_calls[0]:
    messages.append(cast(ChatCompletionMessageParam, response.choices[0].message))
    messages = run_tools(tool_calls, messages)

    final_response = client.chat.completions.create(
        model="minimax/minimax-m2.5", messages=messages
    )
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
