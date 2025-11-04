import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit.components.v1 import html

load_dotenv()

messages = st.container()


def showUserMesg(prompt: str):
    messages.chat_message("user").write(prompt)


def showBotMesg(res):
    messages.chat_message("assistant").write(res)


def getBotResponse(prompt: str):
    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = chat.invoke(prompt)
    return response.content


prompt = st.chat_input("Say something")

if prompt:
    showUserMesg(prompt)
    with st.spinner("Waiting for response..."):
        response = getBotResponse(prompt)
        showBotMesg(response)
