# loading documents from differnt sources into one standardized format (document object)
# each document object has 2 details - content and metadata

from langchain_community.document_loaders import TextLoader

loader = TextLoader(file_path=r"D:\local_synced\workspace\genAI\1.LangChain\7.RAG\cricket.txt", encoding='utf-8')

docs = loader.load()

print("type(docs) - ", type(docs))
print("type(docs[0]) - ", type(docs[0]))
# print("docs[0] - ", docs[0])
print("docs[0].page_content - ", docs[0].page_content)
print("docs[0].metadata - ", docs[0].metadata)