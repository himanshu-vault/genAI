from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

###### objective

# prompt > LLM > parse




#### 1 prompt
prompt = PromptTemplate(
        template='Generate 5 interesting points about {topic}',
        input_variables=['topic']
)

#### 2 model
model = ChatOpenAI(
    model="gpt-4o-2024-08-06",
)

#### 3 parser
parser = StrOutputParser()



#### chain(LCEL)

chain = prompt | model | parser

result = chain.invoke({'topic': 'India'})

print(result)

chain.get_graph().print_ascii()