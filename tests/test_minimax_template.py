import pytest
from typing import List

from minimax_template import run_ralph
from openai.types.chat import ChatCompletionMessageParam


@pytest.mark.integration
def test_calendar_integration():
    messages: List[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": "Create an event called 'Test Event' on March 15th 2026 at 14:00, lasting 1 hour, at 'Test Location'",
        }
    ]
    response = run_ralph(messages)
    assert response is not None
    assert response.choices[0].message.content is not None

    messages = [
        {
            "role": "user",
            "content": "Find an event called 'Test Event' on March 15th 2026 at 14:00 and change its title to 'Updated Test Event'",
        }
    ]
    response = run_ralph(messages)
    assert response is not None
    assert (
        "updated" in response.choices[0].message.content.lower()
        or "edit" in response.choices[0].message.content.lower()
    )

    messages = [
        {
            "role": "user",
            "content": "Find an event called 'Updated Test Event' on March 15th 2026 at 14:00 and delete it",
        }
    ]
    response = run_ralph(messages)
    assert response is not None
    assert (
        "deleted" in response.choices[0].message.content.lower()
        or "delete" in response.choices[0].message.content.lower()
    )
