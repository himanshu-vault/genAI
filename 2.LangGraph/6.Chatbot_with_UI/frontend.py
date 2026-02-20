import streamlit as st
from backend import chatbot
from langchain.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

config = {'configurable' : {'thread_id':1}}

user_input = st.chat_input('Type your message here!')


# loading conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])




if user_input:
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # invoking backedn chatbot
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content


    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
