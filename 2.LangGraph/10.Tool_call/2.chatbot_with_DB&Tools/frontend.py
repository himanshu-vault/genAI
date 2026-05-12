import streamlit as st
from backend import chatbot, retrieve_all_threads
from langchain.messages import HumanMessage, AIMessage
import uuid

###################################################################### Utility functions

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable' : {'thread_id':thread_id}}).values['messages']


###################################################################### Session setup
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = list(retrieve_all_threads())

add_thread(st.session_state['thread_id'])


###################################################################### Side bar UI

st.sidebar.title('LangGraph ChatBot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('my conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assitant'
            temp_messages.append({'role':role, 'content':message.content})

        st.session_state['message_history'] = temp_messages
        



###################################################################### Main UI
# loading conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type your message here!')

if user_input:
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # config setup
    config = {'configurable' : {'thread_id':st.session_state['thread_id']}}

    # invoking backedn chatbot
    stream = chatbot.stream({'messages': [HumanMessage(content=user_input)]}, config=config, stream_mode='messages')
    # ai_message = response['messages'][-1].content


    with st.chat_message('assistant'):
        ai_message = st.write_stream((message_chunk.content for message_chunk, metadata in stream if (isinstance(message_chunk, AIMessage))))
        st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
######################################################################