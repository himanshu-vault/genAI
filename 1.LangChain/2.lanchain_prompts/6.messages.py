from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
import streamlit as st


model = ChatOpenAI(model="gpt-4o-2024-08-06")

chat_history = []

# SystemMessage - To set the behavior of how the system will behave
# HumanMessage  - Human inputs(prompts)
# AI message    - Machine's response


messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content='Tell me about India in 20 words!')
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)




