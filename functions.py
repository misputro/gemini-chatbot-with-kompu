import streamlit as st

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    # Use the session's send_message to get a response and update history
    response = st.session_state.chat_session.send_message(user_query)
    return response.text
