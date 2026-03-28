import os
from collections.abc import AsyncGenerator

import anthropic

from tools.knowledge_base import load_knowledge
from tools.query_filter import FILTER_PROMPT


_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _build_system_prompt() -> str:
    knowledge = load_knowledge()
    return f"""{FILTER_PROMPT}

Below are the complete official rules for Root. Use these as your primary reference when answering questions.

<root_rules>
{knowledge}
</root_rules>"""


async def chat_stream(messages: list[dict]) -> AsyncGenerator[str, None]:
    client = _get_client()
    async with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=_build_system_prompt(),
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text
