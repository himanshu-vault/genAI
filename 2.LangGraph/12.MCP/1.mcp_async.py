from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import asyncio

import requests

from langchain_mcp_adapters.client import MultiServerMCPClient
# langsmith
load_dotenv(override=True)


# MCP client

client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": r"C:/Users/himan/OneDrive/genAI/.venv/Scripts/python.exe",
            "args": [r"C:/Users/himan/OneDrive/genAI/2.LangGraph/12.MCP/main.py"],
        },
        "expense": {
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
        }
    }
)
# model
llm = ChatOpenAI()


# tools
# statndard tool from langchain
search_tool = DuckDuckGoSearchRun(region='us-en')

    
# custom python function as tool
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


###########


# state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    

################## same till here ###################################


async def build_graph():

    # importing tools from an MCP server and binding to LLM
    tools = await client.get_tools()
    
    print("tools - ", tools)
    llm_with_tools = llm.bind_tools(tools)
    
    async def chat_node(state: ChatState):
        """
        LLM node that may answer or request a tool call
        """
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
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
    checkpointer = InMemorySaver()
    chatbot = workflow.compile(checkpointer=checkpointer)
    return chatbot


async def main():
    
    chatbot = await build_graph()
    config = {'configurable' : {'thread_id': 'thread_1'}}
    result = await chatbot.ainvoke(
                    {'messages' : [HumanMessage(content = 'Find the modulus of 12324 and 34 and give answer in cricket commentator style?')]},
                    config=config
                    )
    print('-------------\n', result)
    # print(result['messages'][-1].content)


if __name__ == '__main__':
    asyncio.run(main())