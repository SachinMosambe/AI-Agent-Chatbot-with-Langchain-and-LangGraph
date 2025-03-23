# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Step 1: Setup UI with Streamlit
import streamlit as st
import requests
import json

# Set up page configuration
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

# Sidebar with information
with st.sidebar:
    st.write("### Welcome to AI Chatbot Agent!")
    st.write("Create and interact with AI Agents.")
    st.markdown("---")
    
    if "history" in st.session_state and st.session_state.history:
        st.subheader("Chat History")
        for message in st.session_state.history:
            st.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

# Main UI
st.title("AI Chatbot Agents")
st.write("Define and interact with AI agents!")

if "history" not in st.session_state:
    st.session_state.history = []

# User input fields
system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")
provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

selected_model = st.selectbox("Select Model:", MODEL_NAMES_GROQ if provider == "Groq" else MODEL_NAMES_OPENAI)
allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_input("Enter your query:", placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:8000/chat"

# Check if the user presses Enter (i.e., submits the query)
if user_query.strip():
    payload = {
        "model_name": selected_model,
        "model_provider": provider,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    response = requests.post(API_URL, json=payload)

    try:
        response_data = response.json()  # Ensure JSON parsing
    except json.JSONDecodeError:
        st.error("Error: API did not return valid JSON.")
        st.write("DEBUG: Raw Response:", response.text)
        response_data = {}

    if isinstance(response_data, dict) and "final_response" in response_data:
        st.subheader("Agent Response")
        agent_response = response_data["final_response"]
        st.markdown(agent_response)

        st.session_state.history.append({"role": "user", "content": user_query})
        st.session_state.history.append({"role": "agent", "content": agent_response})
    else:
        st.error("Error: Unexpected API response format.")



