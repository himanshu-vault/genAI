from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv

import requests

# langsmith
load_dotenv(override=True)

# model
llm = ChatOpenAI()


# tools
search_tool = DuckDuckGoSearchRun(region='us-en')

@tool
def calculator_tool(first_num: float, second_num: float, operation: str) -> dict:
    """
    Tool to perform basic arithmetic calculation on two numbers
    supported opeartion - add, sub, mul, div
    """

    try:
        if operation=="add":
            result= first_num+second_num
        elif operation=="sub":
            result= first_num-second_num
        elif operation=="mul":
            result= first_num*second_num
        elif operation=="div":
            if second_num==0:
                return {'error': 'division by zero is not allowed'}
            result= first_num/second_num
        
        return {'operation':operation, 'first_num':first_num, 'second_num':second_num, 'result':result}
    
    except Exception as e:
        return {'Error': str(e)}
    
@tool
def get_stock_price(symbol:str) -> dict:
    """
    get the stock price of the given symbol eg "AAPL", "TSLA"
    from alpha vantage API with the given API KEY
    """
    r = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=H7SWLKFQT5X0T9R2")
    return r.json()
#######


# binding tools with llm
llm = ChatOpenAI()
tools = [search_tool, calculator_tool, get_stock_price]
llm_with_tools = llm.bind_tools(tools)
###########


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
# db checkpointer
checkpointer = SqliteSaver(conn=conn)


# nodes
def chat_node(state: ChatState):
    """
    LLM node that may answer or request a tool call
    """
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

tool_node = ToolNode(tools)

# graph
workflow = StateGraph(ChatState)
workflow.add_node('chat_node', chat_node)
workflow.add_node('tools', tool_node)

# edge
workflow.add_edge(START, "chat_node")
workflow.add_conditional_edges('chat_node', tools_condition)
workflow.add_edge('tools', 'chat_node')


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