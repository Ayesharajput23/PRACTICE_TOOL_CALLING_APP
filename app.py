from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import speech_recognition as sr
import re
import pyttsx3
import streamlit as st
from tools import  calculator, get_latest_news,get_movie_details,get_recipe,get_distance,get_stock_price,get_ip_address ,get_disk_usage,get_time_in_timezone,get_weather
from dotenv import load_dotenv

import os

# Load environment variables from the .env file
load_dotenv()

# Get an environment variable

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


@tool
def handle_audio_input(tool_input: str = None):
    """
    Handles audio input from the user, processes it into text, and generates an AI response with audio playback.
    This function ignores unnecessary words and noise in the speech input.

    Steps:
    1. Listens for audio input using a microphone.
    2. Converts the audio input to text using Google's speech recognition service.
    3. Cleans up the text to remove unwanted words like fillers ("um", "uh").
    4. Generates a response and converts it to audio using text-to-speech.
    5. Plays the generated audio response automatically.
    """
    recognizer = sr.Recognizer()
    
    # Listen for audio input
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        
    try:
        # Convert speech to text
        text_input = recognizer.recognize_google(audio)
        st.success(f"Your text: {text_input}")
        
    
        
        # Simulate AI response (replace with actual LLM logic)
        with st.spinner("AI Responding..."):
            response = agent.invoke(text_input)  # Replace with actual LLM logic
            response = response["output"]
            st.success(f"AI Response: {response}")
            # Clean up the recognized text by removing unwanted words (e.g., fillers, extra spaces)
            cleaned_input = re.sub(r'\b(um|uh|ah|like|so|you know)\b', '', response, flags=re.IGNORECASE)
            cleaned_input = re.sub(r'[^\w\s]', '', cleaned_input)  # Remove unwanted characters like * and _
            

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Select male voice (typically the first or second voice)
            for voice in voices:
                if "male" in voice.name.lower() or "man" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Set the response text and speak it
            engine.say(cleaned_input)
            engine.runAndWait()

    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        st.error(f"Error with the speech recognition service: {e}")


tools = [
    
    calculator,
    get_latest_news,
    get_movie_details,
    get_recipe,
    get_distance,
    get_stock_price,
    get_ip_address,
    get_weather,
    get_time_in_timezone,
    get_disk_usage,
    handle_audio_input



    ]

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" , api_key=GOOGLE_API_KEY)

agent = initialize_agent(tools, llm , agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION )


# import streamlit as st

# Set page config for better look and feel
st.set_page_config(page_title="Practice Tool Calling App", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for more styling
st.markdown(
    """
    <style>
    body {
        background-color: white;
        font-family: 'Arial', sans-serif;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        border-radius: 8px;
        width : 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ccc;
        width: 100%;
    }
    .sidebar .sidebar-content {
        background-color: #e0f7fa;
        font-size: 18px;
        font-weight: bold;
    }
    h1 {
        color: #333;
        font-size: 40px;
        text-align: center;
    }
    h2 {
        color: #555;
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title of the app
st.title("Practice Tool Calling App")

# Sidebar for navigation
st.sidebar.title("Available Tools")
tools = [
    "calculator",
    "get_latest_news",
    "get_movie_details",
    "get_recipe",
    "get_distance",
    "get_stock_price",
    "get_ip_address",
    "get_weather",
    "get_time_in_timezone",
    "get_disk_usage",
    "handle_audio_input ",# Custom tool for handling audio input


]
for tool in tools:
    st.sidebar.write(f"- {tool}")

# Add a brief description on the main page
st.markdown("""
    <h2>Welcome to the Practice Tool Calling App</h2>
    <p>This app uses a powerful language model to help you access various tools. 
    Simply type your question below and let the app automatically select the right tool for you!</p>
""", unsafe_allow_html=True)

# Text input for user to ask a question
user_input = st.text_input("Ask anything", placeholder="Type your question here...")

# Button for submission
if st.button("Submit"):
    # Pass the user input to your LLM to decide the appropriate tool and generate a response
    result = agent.invoke({"input": user_input})
    
    # Display the result from the LLM
    st.write(result["output"])






# Button to start listening
if st.button("Start Speaking"):
    with st.spinner("Listening..."):
        handle_audio_input(tool_input="start")
