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
    stream = chatbot.stream({'messages': [HumanMessage(content=user_input)]}, config=config, stream_mode='messages')
    # ai_message = response['messages'][-1].content


    
    with st.chat_message('assistant'):
        st.write_stream((message_chunk.content for message_chunk, metadata in stream))

