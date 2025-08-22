import streamlit as st
import requests
from typing import List, Dict
import json

# Configure page
st.set_page_config(
    page_title="Your AI Health Assistant",
    page_icon="👩‍⚕️",
    layout="centered"
)

# Constants
API_URL = "http://localhost:8000"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# Custom CSS
st.markdown("""
<style>
    /* Chat container */
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    
    /* Header styling */
    .chat-header {
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Loading animation */
    .stSpinner {
        text-align: center;
        margin: 20px 0;
    }

    /* Message containers */
    div[data-testid="stChatMessage"] {
        margin: 5px 0;
        position: relative;
        padding-left: 48px;  /* Increased space for avatar */
    }

    /* Default message background */
    div[data-testid="stChatMessage"] > div:first-child {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }

    /* User message background */
    div[data-testid="stChatMessage"][data-type="user"] > div:first-child {
        background-color: #f7f6f5 !important;
    }

    /* Avatar container */
    div[data-testid="stChatMessageAvatar"] {
        position: absolute !important;
        left: 0;
        top: 2px;
        width: 38px !important;
        height: 38px !important;
        border-radius: 50%;
        display: flex !important;
        align-items: center;
        justify-content: center;
        z-index: 1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* User avatar specific */
    div[data-testid="stChatMessage"][data-type="user"] div[data-testid="stChatMessageAvatar"] {
        background-color: #f0f2f6;
        border: 2px solid #e0e0e0;
    }

    /* Assistant avatar specific */
    div[data-testid="stChatMessage"][data-type="assistant"] div[data-testid="stChatMessageAvatar"] {
        background-color: #e3f2fd;
        border: 2px solid #bbdefb;
    }

    /* Avatar emoji styling */
    div[data-testid="stChatMessageAvatar"] p {
        margin: 0;
        font-size: 1.3em;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

def get_bot_response(question: str, history: List[Dict]) -> tuple:
    """Get response from the backend API"""
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "conversation_history": history},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["answer"], data.get("sources", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the backend: {str(e)}")
        return None, None

# Title is always visible
st.markdown("<div class='chat-header'><h1>👩‍⚕️ Your AI Health Assistant</h1></div>", unsafe_allow_html=True)

# Show introduction only if conversation hasn't started
if not st.session_state.conversation_started:
    st.markdown("""
    Your personal health guide. Here to answer your questions in simple, clear language.  
    Get trusted medical information instantly, whenever you need it.  

    ✨ **What I Can Help With:**  
    - 🩺 **Symptoms & Conditions** – Understand what your body might be telling you  
    - 💊 **Treatment Options** – Learn about available approaches and therapies  
    - 📖 **Medical Terms Explained** – Break down complex terms into plain language  
    - 🌿 **Everyday Health Tips** – Stay informed and make healthier choices  
    """)


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🏥"):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know about?"):
    # Set conversation as started
    st.session_state.conversation_started = True
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Get bot response
    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("Searching medical knowledge base..."):
            response, sources = get_bot_response(prompt, st.session_state.messages)
            
            if response:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})