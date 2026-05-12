# Based on fixed chunk size

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# load a file
loader = PyPDFLoader(r'D:\local_synced\workspace\genAI\1.LangChain\7.RAG\1.DocLoaders\dl-curriculum.pdf')
# each page becomes a doc
docs = loader.load()

splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separator=''
)

# split a string
# result = splitter.split_text(text)


# splits a list of docs
result = splitter.split_documents(docs)


print('----------------------------------------------------------------------')
print("len(result)   - \n", len(result))
print("result[0]     - \n", result[0])
print("result        - \n", result)
print('----------------------------------------------------------------------')