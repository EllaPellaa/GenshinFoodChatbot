# Main.py
# 
# Endpoints to the tools and LLM implementation

import json
import os
import time
import ollama
from typing import List, Dict, Any
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from tools import get_all_foods_tool, get_food_by_id_tool, get_food_by_name_tool, find_foods_by_ingredient_tool, get_all_ingredients_tool, get_ingredient_by_name_tool, get_ingredients_for_food_tool

app = FastAPI(title="Genshin Impact Recipe Chatbot")

# Allow requests from the React dev server
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
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
    session_id: str = "default"

# ----- Define tools for Ollama -----
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_all_foods",
            "description": "Get all foods from the database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_food_by_id",
            "description": "Get a food item from the database by id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_id": {
                        "type": "integer",
                        "description": "The ID of the food to search for."
                    }
                },
                "required": ["food_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_food_by_name",
            "description": "Get food items from the database by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "The name of the food to search for. Case insensitive, can search with parts of food name."
                    }
                },
                "required": ["food_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_foods_by_ingredient",
            "description": (
                "Find foods that USE a specific ingredient. "
                "Use this when the user asks: 'what foods contain X' or 'what uses carrots'. "
                "Example: 'What foods use carrots?' → use this tool."
                "Input is an ingredient name, output is a list of foods."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ingredient_name": {
                        "type": "string",
                        "description": "Exact or partial ingredient name (e.g. 'carrot', 'crab roe')."
                    }
                },
                "required": ["ingredient_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_ingredients",
            "description": "Get all ingredients from the database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ingredient_by_name",
            "description": "Get ingredient from the database by name. ",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "The name of the ingredient to search for. Case insensitive, has to be exact with no plural etc. (carrots -> carrot before searching)"
                    }
                },
                "required": ["food_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ingredients_for_food",
            "description": (
                "Get INGREDIENTS of a specific FOOD. "
                "Use this when the user asks: 'what ingredients does X have' or 'what is in X'. "
                "Example: 'What ingredients are in Sticky Honey Roast?' → use this tool."
                "Input is a food name, output is a list of ingredients."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "The name of the food that's ingredients are fetched."
                    }
                },
                "required": ["food_name"]
            }
        }
    },
]

TOOL_IMPLEMENTATIONS = {
    "get_all_foods": get_all_foods_tool,
    "get_food_by_id": get_food_by_id_tool,
    "get_food_by_name": get_food_by_name_tool,
    "find_foods_by_ingredient": find_foods_by_ingredient_tool,
    "get_all_ingredients": get_all_ingredients_tool,
    "get_ingredient_by_name": get_ingredient_by_name_tool,
    "get_ingredients_for_food": get_ingredients_for_food_tool
}

# ----- Execute the tool calls -----
def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> str:
    """
    Execute a tool function and return result as string.
    Args:   tool_name - Name of the tool that's to be executed
            tool_args - Arguments of the tool
    Returns: The tool result as JSON string
    """
    if tool_name not in TOOL_IMPLEMENTATIONS:
        return json.dumps({"error": f"Tool '{tool_name}' not found"})
    
    try:
        tool_function = TOOL_IMPLEMENTATIONS[tool_name]
        # Actually calling the tool itself
        result = tool_function(**tool_args)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Tool execution failed: {str(e)}"})




# ----- Processing tool calls -----
def process_tool_calls(messages: List[Dict[str, str]], response: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Handling tool calls.
    Parameters: messages - conversation history
                response - Response from Ollama containing tool call
    Returns: Updates messages-list with tool call results
    """
    if not response["message"].get("tool_calls"):
        return messages
    
    # Add the assistant's previous response with tool calls to the messages
    messages.append(response["message"])

    # Execute each tool call
    for tool_call in response["message"]["tool_calls"]:
        tool_name = tool_call["function"]["name"]
        tool_args = tool_call["function"]["arguments"]
        print("TOOL CALLS:", response["message"].get("tool_calls"))

        # Execute the tool
        tool_result = execute_tool(tool_name, tool_args)

        # Add tool result to the previous conversation
        messages.append({
            "role": "tool",
            "content": tool_result
        })

    return messages


# ----- Endpoints -----

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Normal chat with no stream
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Non-streaming endpoint - returns the full response at once.
    Tool calling is in a loop until no more tools are needed.
    """
    if not check_rate_limit(request.session_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in a moment.")
    
    # Give the LLM a prompt.
    system_prompt = """
    You are a database assistant for looking for foods and ingredients from the game Genshin Impact.

    IMPORTANT RULES:
    - If the user asks about ingredients (e.g. "what foods use carrots"), you MUST call find_food_by_ingredient.
    - Never answer from memory when tools are available.
    - Always prefer tools for database questions.

    Tool usage rules:
    - If the user gives an INGREDIENT and asks for foods → use find_foods_by_ingredient
    - If the user gives a FOOD and asks for ingredients → use get_ingredients_for_food

    Never confuse these two directions.
    """

    # Build the full conversation: sys prompt + history + new user message
    messages = [{"role": "system", "content": system_prompt}] + request.history + [{"role": "user", "content": request.message}]
    
    # Looping the AI until it doesn't need the tools, make sure it doesn't start looping more than 5 times (This many tools most likely not needed).
    max_steps = 5
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            break
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOLS
        )

        if not response["message"].get("tool_calls"):
            final_text = response["message"]["content"]
            return {
                "response": final_text
            }
        
        messages = process_tool_calls(messages, response)

# Chat with stream
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint using Server-Sent Events (SSE)
    """

    if not check_rate_limit(request.session_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    
    # ----- Tool calls before generating an answer with streaming -----
    #       Streaming not needed when calling tools, since the tool calling just passes along the full answer
    #       to the next loop without giving it to user.

    # Give the LLM a prompt so it functions better.
    system_prompt = """
    You are a database assistant for looking for foods and ingredients from the game Genshin Impact.

    IMPORTANT RULES:
    - If the user asks about ingredients (e.g. "what foods use carrots"), you MUST call find_food_by_ingredient.
    - Never answer from memory when tools are available.
    - Always prefer tools for database questions.

    Tool usage rules:
    - If the user gives an INGREDIENT and asks for foods → use find_foods_by_ingredient
    - If the user gives a FOOD and asks for ingredients → use get_ingredients_for_food

    Never confuse these two directions.
    """

    # Build the full conversation: sys prompt + history + new user message
    messages = [{"role": "system", "content": system_prompt}] + request.history + [{"role": "user", "content": request.message}]

    # Looping the AI until it doesn't need the tools, make sure it doesn't start looping more than 5 times (This many tools most likely not needed).
    max_steps = 5
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            break
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOLS
        )

        # Break from loop if tool calls not needed
        if not response["message"].get("tool_calls"):
            break
        
        # Call tools if needed
        messages = process_tool_calls(messages, response)

    def generate():
        # We already have the messages from earlier, no need to define that again inside generate
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOLS,
            stream=True
        )

        for chunk in response:
            content = chunk["message"]["content"]
            if content:
                yield f"data: {json.dumps({'type': 'text', 'content': content})}\n\n"

        # Send event to indicate the stream is done
        done_event = json.dumps({
            "type": "done",
        })
        yield f"data: {done_event}\n\n"


    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # tells nginx: don't buffer this
        },
    )