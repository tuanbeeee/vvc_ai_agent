# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time
from main import run_agent   # Import your agent logic from main.py

app = FastAPI(title="My AI Agent for OpenWebUI")

# ---------------- Request/Response Models ----------------
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]

@app.get("/api/v1/models")
def list_models():
    return {"data": [{"id": "VVC_AI_AGENTS"}]}

@app.post("/api/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    # get last user message
    user_msg = None
    for msg in reversed(req.messages):
        if msg.role == "user":
            user_msg = msg.content
            break
    if not user_msg:
        raise HTTPException(status_code=400, detail="No user input")

    # run your AI agent
    reply = run_agent(user_msg)

    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": reply},
                "finish_reason": "stop",
            }
        ],
    }
