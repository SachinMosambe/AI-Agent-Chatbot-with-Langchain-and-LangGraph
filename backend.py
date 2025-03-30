# Step 1: Setup Pydantic Model (Schema Validation)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ai_agent import get_response_from_ai_agent
from constants import HOST , BACKEND_PORT
# Define request structure
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# Allowed model names
ALLOWED_MODEL_NAMES = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gpt-4o-mini"]

# Initialize FastAPI app
app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState): 
    """
    API Endpoint to interact with the Chatbot using LangGraph and optional web search.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid AI model."}
    
    if request.model_provider not in ["Groq", "OpenAI"]:
        return {"error": "Invalid model provider. Choose either 'Groq' or 'OpenAI'."}

    if not request.messages:
        return {"error": "Message list cannot be empty."}

    # Extract data
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Get AI response
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response

# Step 3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=BACKEND_PORT)

