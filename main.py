import streamlit as st
from chatbot import init_chat, ask_question


st.title("Ask Me Anything!")
st.caption("A chatbot powered by Google Gemini")

st.sidebar.title("Settings")
st.sidebar.text_input("Enter your groq API key")
agent = st.sidebar.selectbox("Select AI Agent",["English Translator","Spoken English Teacher","Travel Guide","Storyteller", "Interviewer"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(placeholder="What is your question?")
messages = st.container()
if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)
    
    if len(st.session_state.messages) == 1:
       response = init_chat(agent, question)
    else:
       response = ask_question(agent, question)
   
    st.session_state.messages.append({"role":"assistant","content":response})


    with st.chat_message("assistant"):
        st.markdown(response)

