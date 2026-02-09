# loading documents from differnt sources into one standardized format (document object)
# each document object has 2 details - content and metadata

from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, WebBaseLoader, CSVLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

#model
model = ChatOpenAI()

parser = StrOutputParser()

prompt = PromptTemplate(
        template = "Answer the following question \n {question} from the following text \n {text}",
        input_variables=['question', 'text']
)

### loading csv(every row will become a separate doc)
loader = CSVLoader(r"D:\local_synced\workspace\genAI\1.LangChain\7.RAG\1.DocLoaders\Social_Network_Ads.csv")
docs = loader.load()


for doc in docs:
    print(doc, '\n----------------------------------------')

print("type(docs) -----------------------\n ", type(docs))
print("type(docs[0]) -----------------------\n ", type(docs[0]))
print("docs[0] -----------------------\n ", docs[0])
print("docs[0].page_content -----------------------\n ", docs[0].page_content)
print("docs[0].metadata -----------------------\n ", docs[0].metadata)



# chain = prompt | model | parser

# result = chain.invoke({'question':"whats the RAM", 'text':docs})

# print(result)