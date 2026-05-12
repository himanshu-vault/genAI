from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 


model = ChatOpenAI(model="gpt-4o-2024-08-06")

# chat Template

chatTemplate = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human',  '{query}')
])


# load history
chat_history = []
with open(r'D:\local_synced\workspace\genAI\2.lanchain_prompts\chat_history.txt') as f:
    chat_history.extend(f.readlines())

# print(chat_history)


# # create final prompt
prompt = chatTemplate.invoke(
            {'chat_history':chat_history, 
            'query':'Where is my refund?'
            }
    )

print(prompt)
 