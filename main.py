import streamlit as st
from genai import ask_question


st.title("Ask Me Anything!")
st.caption("A chatbot powered by Google Gemini")


agent = st.selectbox("Select AI Agent",["English Translator","Spoken English Teacher","Travel Guide","Storyteller", "Interviewer"])
question = st.text_input("What is your question?")

if question:
    response = ask_question(agent, question)
    st.write(response)
