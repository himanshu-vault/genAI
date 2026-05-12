from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3



# model
llm = ChatOpenAI()


# state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState) -> ChatState:
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : response}
#

# db creation
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
#



# checkpointer
checkpointer = SqliteSaver(conn=conn)

# graph
workflow = StateGraph(ChatState)

# nodes
workflow.add_node('chat_node', chat_node)

# edge
workflow.add_edge(START, 'chat_node')
workflow.add_edge('chat_node', END)


# compile
chatbot = workflow.compile(checkpointer=checkpointer)



# config = {'configurable' : {'thread_id': 'thread_2'}}
# result = chatbot.invoke(
#                 {'messages' : [HumanMessage(content = 'My Name is Himanshu')]},
#                 config=config
#                 )
# print(result)


# config = {'configurable' : {'thread_id': 'thread_2'}}
# result = chatbot.invoke(
#                 {'messages' : [HumanMessage(content = 'What good in the capital of India, Say my name while answering!')]},
#                 config=config
#                 )
# print(result)

def retrieve_all_threads():
    all_threads = set()
    for i, checkpoint in enumerate(checkpointer.list(None)):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return(all_threads)



