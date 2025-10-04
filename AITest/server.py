# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from starlette.responses import StreamingResponse # Import StreamingResponse
import time
from main import run_agent   # Import your agent logic from main.py
import json

app = FastAPI(title="My AI Agent for OpenWebUI")

# ---------------- Request/Response Models ----------------
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]

# Helper to format chunks into the OpenAI SSE format
def format_sse_chunk(chunk_id: str, model_id: str, text: str, finish_reason: str = None) -> str: # type: ignore
    # This structure is what OpenWebUI/OpenAI API expects for streaming
    data = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model_id,
        "choices": [
            {
                "index": 0,
                "delta": {"content": text},
                # Only include finish_reason in the last chunk
                "finish_reason": finish_reason,
            }
        ],
    }
    # return "data: " + json.dumps(data) + "\n\n"
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

@app.get("/api/v1/models")
def list_models():
    return {"data": [{"id": "MyHa"}]}

# The endpoint is now a standard function, but it returns a StreamingResponse
@app.post("/api/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    # get last user message (logic remains the same)
    user_msg = None
    for msg in reversed(req.messages):
        if msg.role == "user":
            user_msg = msg.content
            break
    if not user_msg:
        raise HTTPException(status_code=400, detail="No user input")

    # Define the generator function for the stream
    def generate_stream():
        # Unique ID for this conversation stream
        stream_id = f"chatcmpl-{int(time.time())}"
        
        # Run the agent, which now returns a generator (or iterable)
        stream_generator = run_agent(user_msg)

        # Yield each text chunk formatted as an SSE
        for text_chunk in stream_generator:
            yield format_sse_chunk(stream_id, req.model, text_chunk)
            
        # Yield the final chunk indicating the end of the stream
        yield format_sse_chunk(stream_id, req.model, "", finish_reason="stop")
        yield "data: [DONE]\n\n" # Required by some clients/OpenWebUI

    # Return the StreamingResponse
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream" # Set content type for Server-Sent Events (SSE)
    )
