import streamlit as st

st.title("Chat Example")

# Create a scrollable text area for the chat
chat_log = st.text_area("Chat Log", height=200, max_chars=10000, key="chat_log")

# Add user input field
user_input = st.text_input("User Input", key="user_input")

# Add a button to send user input
if st.button("Send"):
    # Append the user input to the chat log
    chat_log += f"\nUser: {user_input}"

# Display the updated chat log
st.text_area("Updated Chat Log", value=chat_log, height=200, max_chars=10000)
