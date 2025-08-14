
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
search_tool = TavilySearchResults(max_results=2)


system_prompt = "Act as an AI chatbot who is smart and friendly."

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    """Generates response from the AI agent with optional web search."""
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)
    else:
        return {"error": "Invalid provider"}

    tools = [TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(model=llm, tools=tools, state_modifier=system_prompt)


    user_message = query[-1] if isinstance(query, list) and query else query

    state = {"messages": [user_message]}
    response = agent.invoke(state)


    messages = response.get("messages", [])
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]


    final_response = ai_messages[-1] if ai_messages else "I'm sorry, I couldn't generate a response."

    return {"final_response": final_response}


