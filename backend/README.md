## Project Description

This project is a chatbot, that can search for foods, their ingredients and ingredient amounts from the game Genshin Impact.
This idea was chosen, because the game itself doesn't have the capability of searching for recipes by ingredient.
You can ask the chatbot, that is using local LLM model (ollama qwen2.5:7b used in my case), to look for recipes by name and their required ingredients and amounts, or you can look for recipes by the wanted ingredients (recipes containing carrots, for example).

## Running the local AI

This chatbot uses qwen2.5:7b local ai via ollama. You can start/download the local ai from the console with "ollama run qwen2.5:7b"
(download ollama itself first before running this). This particular model runs fairly well with 16GB RAM and a RTX 2070 graphic card.

## Running the project

You can set up and start the backend with the commands below.

### Setting up the backend environment

You can create a python virtual environment with ***python -m venv venv***. *You must be in the backend-folder before running this command.*

Start the virtual environment with ***./venv/Scripts/activate***

Download the dependencies with ***pip install -r requirements.txt***

Create the database with ***python create_food_db.py***

Start the backend with ***uvicorn main:app --reload***

## Architecture Overview
- backend, frontend, LLM provider, and how they connect. A simple text description is fine (e.g., "React → FastAPI → Gemini API"). A diagram is a bonus.

React -> FastAPI -> Ollama local AI -> Tools -> Services -> Database

## Technical Choises
- which libraries/frameworks you used and why (e.g., "LangGraph for multi-step reasoning because our app needs conditional routing between tools") 

## Setup and Running Instructions
 — step by step: clone, install dependencies, set environment variables, start the app. Another developer should be able to run your project by following these instructions.

## Known Limitations
— what doesn’t work, what’s hardcoded, what would need to change for production use. Be honest — this section is valued.

## AI tools used
Used ChatGPT for making the database structure correctly and inserting some example data to the database (although had to fix the data manually due to wrong information). 

Asked Claude for help with implementing Ollama local AI to the main.py instead of a Gemini model. 