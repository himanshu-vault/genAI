# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# model = ChatOpenAI()
model = ChatAnthropic(model="claude-sonnet-4-5")

parser = StrOutputParser()

template = PromptTemplate.from_template("{question}")

chain = template | model | parser
result = chain.invoke({"question":"What is the capital of India?"})
print(result)