# Run Workflow

## Purpose
Orchestrate all tools into the FastAPI application — the main entry point.

## Strategy
- FastAPI app serves:
  - `GET /` — the chat UI (HTML frontend)
  - `POST /chat` — accepts JSON `{messages: [{role, content}]}`, returns `{response: string}`
  - `GET /health` — health check for Railway
- On startup, load the knowledge base once
- Each `/chat` request passes through the chat engine which includes the query filter via system prompt
- Serve static files for the frontend

## Deployment
- Railway runs the app via `uvicorn`
- Port is read from `PORT` env var (Railway sets this), defaulting to 8000
- API key is read from `ANTHROPIC_API_KEY` env var
