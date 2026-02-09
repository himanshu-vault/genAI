# loading documents from differnt sources into one standardized format (document object)
# each document object has 2 details - content and metadata

from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# #model
# model = ChatOpenAI()

# parser = StrOutputParser()

# prompt = PromptTemplate(
#         template = "Write a summary for the following content \n {content}",
#         input_variables=['content']
# )

### loading text from file
loader = DirectoryLoader(
    path=r'D:\local_synced\workspace\genAI\1.LangChain\7.RAG\books',
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load()
#lazy load changes output of docs from list to generator


print("type(docs) - ", type(docs))

for doc in docs:
    print(doc.metadata)


# print("type(docs[0]) - ", type(docs[0]))
# print("docs[0] - ", docs[0])
# print("docs[0].page_content - ", docs[0].page_content)
# print("docs[0].metadata - ", docs[0].metadata)

