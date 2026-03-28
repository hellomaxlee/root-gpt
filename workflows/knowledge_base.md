# Knowledge Base Workflow

## Purpose
Load and serve the Root board game rules as context for the chatbot's system prompt.

## Strategy
- Read pre-extracted text files from the `knowledge/` directory at startup
- Combine both sources (Learning to Play rules + The Law of Root) into a single comprehensive knowledge string
- Cache the loaded text in memory so it's read once, not per-request
- Expose a simple function that returns the full rules text for injection into Claude's system prompt

## Input
- `knowledge/root_rules.txt` — extracted from the Learning to Play PDF
- `knowledge/law_of_root.txt` — extracted from The Law of Root PDF

## Output
- A single string containing the complete Root rules knowledge base
