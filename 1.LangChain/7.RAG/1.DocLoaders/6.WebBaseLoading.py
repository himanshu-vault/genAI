# loading documents from differnt sources into one standardized format (document object)
# each document object has 2 details - content and metadata

from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, WebBaseLoader
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

### loading text web
url = r"https://www.flipkart.com/apple-macbook-air-m2-16-gb-256-gb-ssd-macos-sequoia-mc7x4hn-a/p/itmdc5308fa78421?pid=COMH64PY76CJKBYU&lid=LSTCOMH64PY76CJKBYUOL7TOK&marketplace=FLIPKART&store=6bo%2Fb5g&spotlightTagId=default_BestsellerId_6bo%2Fb5g&srno=b_1_1&otracker=browse&fm=organic&iid=4e90df79-7577-40c0-8f36-625b972cbbe3.COMH64PY76CJKBYU.SEARCH&ppt=sp&ppn=productListView&ssid=hakot7x7740000001770118574641"
loader = WebBaseLoader(url)
docs = loader.load()

# print("type(docs) -----------------------\n ", type(docs))
# print("type(docs[0]) -----------------------\n ", type(docs[0]))
# print("docs[0] -----------------------\n ", docs[0])
# print("docs[0].page_content -----------------------\n ", docs[0].page_content)
# print("docs[0].metadata -----------------------\n ", docs[0].metadata)



chain = prompt | model | parser

result = chain.invoke({'question':"whats the RAM", 'text':docs})

print(result)