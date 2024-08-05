from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage,SystemMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agents import get_agent_instr

load_dotenv()
model = ChatGroq(model="Gemma2-9b-It")
parser = StrOutputParser()
store={}
trimmer = trim_messages(
    max_tokens=4000,
    strategy="last",
    token_counter=model,
    include_system=True
)

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if(session_id not in store):
        store[session_id]=ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","{agent_instr}"),
        MessagesPlaceholder(variable_name="messages")
    ]
)
chain = prompt | trimmer| model | parser

config = {"configurable":{"session_id":"chat1"}}
with_message_history=RunnableWithMessageHistory(chain,get_session_history, input_messages_key="messages")

def init_chat(agent, query):
    agent_instr = get_agent_instr(agent)
    return with_message_history.invoke({"messages": [HumanMessage(content=query)],"agent_instr":agent_instr},config=config)

def ask_question(agent, query):
    agent_instr = get_agent_instr(agent)
    return  with_message_history.invoke({"messages": [HumanMessage(content=query)],"agent_instr":agent_instr},config=config)

