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

docs = loader.load()

print("len(docs) - ", len(docs))
print("type(docs) - ", type(docs))
print("type(docs[0]) - ", type(docs[0]))
# print("docs[0] - ", docs[0])
# print("docs[0].page_content - ", docs[0].page_content)
print("docs[0].metadata - ", docs[0].metadata)


# # #### chain
# chain = prompt | model | parser

# # #### invoke chain and passign page_content
# result = chain.invoke({'content': docs[0].page_content})

# print(result)




# for pdfs with tables - pdfplumer loader 
# for images - unstructured pdf loader / amazontextractpdfloader
# layout and image - pymupdfloader
# structure extraction  - unstructuredPDF loader~



# https://docs.langchain.com/oss/python/integrations/document_loaders