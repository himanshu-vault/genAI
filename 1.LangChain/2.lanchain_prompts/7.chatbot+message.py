from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
import streamlit as st


model = ChatOpenAI(model="gpt-4o-2024-08-06")

chat_history = [
    SystemMessage(content="You are a helpful assistant")
]

while True:
    user_input = input("You: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print('AI:', result.content)

print(chat_history)




