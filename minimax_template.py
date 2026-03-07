import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import cast

load_dotenv()

client: OpenAI | None = None


def get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_KEY"),
        )
    return client


from tool_calls import get_tools, run_tools
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
    ChatCompletion,
)

tools = get_tools()


def run_ralph(messages: list[ChatCompletionMessageParam]) -> ChatCompletion | None:
    response: ChatCompletion | None = None
    for _ in range(10):
        response = get_client().chat.completions.create(
            model="minimax/minimax-m2.5", messages=messages, tools=tools
        )

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            break

        messages.append(cast(ChatCompletionMessageParam, response.choices[0].message))
        result = run_tools(tool_calls, messages)
        messages = result[0]
        tool_calling = result[1]

    return response
