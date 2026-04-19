## Project Description

This project is a chatbot, that can search for foods, their ingredients and ingredient amounts from the game Genshin Impact.
This idea was chosen, because the game itself doesn't have the capability of searching for recipes by ingredient.
You can ask the chatbot, that is using local LLM model (ollama qwen2.5:7b used in my case), to look for recipes by name and get their required ingredients and amounts, or you can look for recipes by the wanted ingredients (recipes containing carrots, for example).

### Setup and Running Instructions

Clone the repository locally with: ***git clone https://github.com/EllaPellaa/GenshinFoodChatbot.git***

There are currently no environment variables, since the local model didn't require api keys etc. to run.

##### Running the local AI

This chatbot uses qwen2.5:7b local ai via ollama. You can start/download the local ai from the console with "ollama run qwen2.5:7b"
(download ollama itself first before running this). This particular model runs fairly well with 16GB RAM and a RTX 2070 graphic card.

You can download ollama to your machine from ***https://www.ollama.com/download***

##### Setting up the backend environment

You can create a python virtual environment with ***python -m venv venv***. **You must be in the backend-folder before running this command.**

Start the virtual environment with ***./venv/Scripts/activate***

Download the dependencies with ***pip install -r requirements.txt***

Create the database with ***python create_food_db.py***

Start the backend with ***uvicorn main:app --reload***


##### Setting up the frontend environment

Install the dependencies by running ***npm install***

Run the frontend application with ***npm run dev***

**You need to be in the frontend-folder before running these commands**

## Architecture Overview

React -> FastAPI -> Ollama local AI -> Tools -> Services (-> Helpers) -> Database

## Technical Choises
- which libraries/frameworks you used and why (e.g., "LangGraph for multi-step reasoning because our app needs conditional routing between tools") 

This application used react

## Known Limitations
— what doesn’t work, what’s hardcoded, what would need to change for production use. Be honest — this section is valued.

When moving to production, this application would have to be changed to run on Gemini/other LLM that is in the cloud and not a local one. The solution of using a local LLM for this project was out of curiosity and the limited LLM calls of free-tier models, which was not ideal for debuggine etc. purposes. 

The database would also be in the cloud and not a local file, and it would be good to have some kind of interface for adding more recipes, ingredients etc. into the database. The database would need to be updated just about every game update due to new recipes in the game. The chatbot also gives a lot of unneeded information when getting the data from the database, even when explicitly asked to only provide dish names etc. as the final answer.

The model might hallucinate occasionally, even when given completely valid and related prompts. Some of the most obivious causes for hallucinations have been fixed, but more undiscovered bugs undoubtedly exist and would have to be fixed before production.

There would also need to be some kind of implementation for different users and message/token limits for each user, so the costs don't skyrocket. 

The model currently doesn't answer completely unrelated questions, but some additional guardrails for this wouldn't do any harm.

## AI tools used
Used ChatGPT for making the database structure correctly and inserting some example data to the database (although had to fix the data manually due to wrong information). 

Asked Claude for help with implementing Ollama local AI to the main.py instead of a Gemini model. 

Used ChatGPT to improve the prompts and tool descriptions given to the LLM in order to get more accurate answers.