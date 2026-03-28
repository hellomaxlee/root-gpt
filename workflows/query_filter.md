# Query Filter Workflow

## Purpose
Ensure that only Root-related queries are processed by the chatbot. Reject off-topic questions.

## Strategy
- Build a system prompt instruction that tells Claude to only answer Root-related questions
- If a user asks something unrelated to the Root board game, Claude should politely decline and redirect
- This is enforced via the system prompt rather than pre-filtering, so Claude can use judgment on edge cases (e.g., general board game strategy that applies to Root)

## Behavior
- Accept: Rules questions, strategy advice, faction breakdowns, setup help, card explanations, scoring clarifications
- Reject: Anything not related to the Root board game (coding help, general chat, other games, etc.)
- Edge cases: General board game concepts are okay if the user is asking in the context of Root
