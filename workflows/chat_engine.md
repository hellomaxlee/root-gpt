# Chat Engine Workflow

## Purpose
Handle conversation with the user by sending messages to Claude API with the Root rules as context.

## Strategy
- Accept a conversation history (list of messages) from the client
- Build a system prompt that includes:
  1. The chatbot's persona (Root expert, friendly, concise)
  2. The full rules knowledge base
  3. The query filter instructions (reject off-topic)
- Send the conversation to Claude API via the Anthropic SDK
- Return Claude's response text

## Parameters
- `messages`: List of {role, content} dicts representing the conversation
- Returns: The assistant's response string

## Model
- Use `claude-sonnet-4-20250514` for fast, cost-effective responses with strong reasoning
