import streamlit as st
from agent import ChatAgent  # Import our new agent class

# --- Page Configuration ---
st.set_page_config(
    page_title="LangGraph Agent Chat",
    page_icon="🤖"
)

st.title("🤖 LangGraph Agent Chat")
st.caption("Ask me to multiply, square, or anything else!")

# --- State Management ---
# Initialize chat history and agent in session_state
# This ensures they persist across reruns

if "agent" not in st.session_state:
    # Initialize the agent only once
    st.session_state.agent = ChatAgent()

if "messages" not in st.session_state:
    # Initialize the chat history
    st.session_state.messages = []

# --- UI Functions ---


def display_chat_history():
    """Displays the entire chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_chat_input(prompt: str):
    """
    Handles a new user prompt.
    1. Adds user message to state and UI.
    2. Gets agent's response.
    3. Adds agent's response to state and UI.
    """
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display agent response
    with st.chat_message("assistant"):
        with st.spinner("Waiting for response..."):
            # Get the agent from session state
            agent = st.session_state.agent

            # Get the response
            response = agent.invoke(prompt)

            st.markdown(response)

    # Add agent response to state
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

# --- Main App Logic ---


# Display the existing chat history
display_chat_history()

# Get new user input
if prompt := st.chat_input("Say something"):
    handle_chat_input(prompt)
