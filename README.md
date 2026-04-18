## Project Description

This project is a chatbot, that can search for foods, their ingredients and ingredient amounts from the game Genshin Impact.
This idea was chosen, because the game itself doesn't have the capability of searching for recipes by ingredient.
You can ask the chatbot, that is using local LLM model (ollama qwen2.5:7b), to look for recipes by name and their required ingredients and amounts, or you can look for recipes by the wanted ingredients (recipes containing carrots, for example).

## Running the local AI

This chatbot uses qwen2.5:7b local ai via ollama. You can start/download the local ai from the console with "ollama run qwen2.5:7b"
(download ollama itself first before running this). This particular model runs fairly well with 16GB RAM and a RTX 2070 graphic card.

## Architecture Overview
- backend, frontend, LLM provider, and how they connect. A simple text description is fine (e.g., "React → FastAPI → Gemini API"). A diagram is a bonus.

## Technical Choises
- which libraries/frameworks you used and why (e.g., "LangGraph for multi-step reasoning because our app needs conditional routing between tools") 

## Setup and Running Instructions
 — step by step: clone, install dependencies, set environment variables, start the app. Another developer should be able to run your project by following these instructions.

## Known Limitations
— what doesn’t work, what’s hardcoded, what would need to change for production use. Be honest — this section is valued.

## AI tools used
Used ChatGPT for making the database structure correctly.
