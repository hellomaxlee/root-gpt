import os

import anthropic

from tools.knowledge_base import load_knowledge
from tools.query_filter import FILTER_PROMPT


_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _build_system_prompt() -> str:
    knowledge = load_knowledge()
    return f"""{FILTER_PROMPT}

Below are the complete official rules for Root. Use these as your primary reference when answering questions.

<root_rules>
{knowledge}
</root_rules>"""


def chat(messages: list[dict]) -> str:
    client = _get_client()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=_build_system_prompt(),
        messages=messages,
    )
    return response.content[0].text
