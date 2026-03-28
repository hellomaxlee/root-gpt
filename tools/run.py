import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tools.chat_engine import chat_stream
from tools.knowledge_base import load_knowledge

app = FastAPI(title="Root Bot")

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    messages: list[dict]


@app.on_event("startup")
async def startup():
    load_knowledge()


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = _TEMPLATES_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    def generate():
        for chunk in chat_stream(request.messages):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
