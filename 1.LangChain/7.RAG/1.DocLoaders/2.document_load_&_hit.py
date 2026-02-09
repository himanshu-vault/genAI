# loading documents from differnt sources into one standardized format (document object)
# each document object has 2 details - content and metadata

from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

#model
model = ChatOpenAI()

parser = StrOutputParser()

prompt = PromptTemplate(
        template = "Write a summary for the following poem \n {poem}",
        input_variables=['poem']
)

### loading text from file
loader = TextLoader(file_path=r"D:\local_synced\workspace\genAI\1.LangChain\7.RAG\cricket.txt", encoding='utf-8')
docs = loader.load()

# print("type(docs) - ", type(docs))
# print("type(docs[0]) - ", type(docs[0]))
# print("docs[0] - ", docs[0])
# print("docs[0].page_content - ", docs[0].page_content)
# print("docs[0].metadata - ", docs[0].metadata)


# #### chain
chain = prompt | model | parser

# #### invoke chain and passign page_content
result = chain.invoke({'poem': docs[0].page_content})

print(result)