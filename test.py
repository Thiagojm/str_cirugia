import streamlit as st

# Define a class to handle session state
class SessionState:
    def __init__(self):
        self.messages = []

# Create or get the session state
if "session" not in st.session_state:
    st.session_state.session = SessionState()

# Example conversation
conversation = st.session_state.session.messages

# Get user input
user_input = st.text_input("Your message")

# Add user input to the conversation
if user_input:
    conversation.append({"user": "User", "message": user_input})

# Display the conversation
for entry in conversation:
    user = entry["user"]
    message = entry["message"]
    st.text(f"{user}: {message}")

# Update the session state
st.session_state.session.messages = conversation