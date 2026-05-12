from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages


llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState) -> ChatState:
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : response}


# checkpointer
checkpointer = InMemorySaver()

# graph
workflow = StateGraph(ChatState)

# nodes
workflow.add_node('chat_node', chat_node)

# edge
workflow.add_edge(START, 'chat_node')
workflow.add_edge('chat_node', END)


# compile
chatbot = workflow.compile(checkpointer=checkpointer)

config = {'configurable' : {'thread_id': 'thread_1'}}
result = chatbot.invoke(
                {'messages' : [HumanMessage(content = 'Capital of India')]},
                config=config
                )

messages = chatbot.get_state(config=config).values['messages']

# for message in messages:
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", type(message))
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", message.content)

