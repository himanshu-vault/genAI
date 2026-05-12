from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 



model = ChatOpenAI(model="gpt-4o-2024-08-06")

# chatTemplate = ChatPromptTemplate([
#     SystemMessage(content="You are a helpful {domain} expert"),
#     HumanMessage(content='Explain in simple terms about the {topic}')
# ])


chatTemplate = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful {domain} expert'),
    ('human',  'Explain in simple terms about the {topic}')
])

prompt = chatTemplate.invoke({'domain':'cricket', 'topic':'Dusra'})

print(prompt)