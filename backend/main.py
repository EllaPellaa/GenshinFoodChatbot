# Main.py
# 
# Endpoints to the tools and LLM implementation

import json
import os
import time
import ollama
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="Genshin Impact Recipe Chatbot")

# Allow requests from the React dev server
app.add_middleware(
  CORSMiddleware,
  allow_origins["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# ----- Rate Limiting -----
# In production: use Redis + sliding window per authenticated user
RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW = 60

request_timestamps: dict[str, list[float]] = defaultdict(list)

def check_rate_limit(session_id: str) -> bool:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    # Drop timestamps outside the window
    request_timestamps[session_id] = [
        t for t in request_timestamps[session_id] if t > window_start
    ]
    if len(request_timestamps[session_id]) >= RATE_LIMIT_REQUESTS:
        return False
    request_timestamps[session_id].append(now)
    return True

# ----- Request model -----

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]

# ----- Endpoints -----
