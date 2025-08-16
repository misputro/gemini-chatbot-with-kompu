import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from functions import map_role, fetch_gemini_response

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat bersama Kompu!",
    page_icon="🤖",  # Favicon emoji
    layout="wide",  # Use wide layout to control width with columns
)

# Custom CSS to add a border to the form and color the text box
st.markdown("""
<style>
    /* Target the container of the middle column to act as a form border */
    div[data-testid="column"]:nth-of-type(2) > div[data-testid="stVerticalBlock"] {
        border: 2px solid #90caf9; /* A nice light blue */
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Style the chat input text area with a light blue background */
    div[data-testid="stChatInput"] textarea {
        background-color: #e3f2fd;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Create columns for a centered layout with 80% width
_, center_col, _ = st.columns([0.1, 0.8, 0.1])

with center_col:
    # Display the chatbot's title on the page
    st.title("🤖 Chat bersama Kompu")

    # Display the chat history from the Gemini chat session
    for msg in st.session_state.chat_session.history:
        with st.chat_message(map_role(msg.role)):
            st.markdown(msg.parts[0].text)

    # Input field for user's message
    if user_input := st.chat_input("Ask Kompu..."):
        # Add user's message to chat and display it
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send user's message to Gemini and get the response
        gemini_response = fetch_gemini_response(user_input)

        # Display Gemini's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response)
