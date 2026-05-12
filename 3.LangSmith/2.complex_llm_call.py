from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


load_dotenv()

#### 1st prompt - detailed report
prompt1 = PromptTemplate(
        template='Generate a detailed report {topic}',
        input_variables=['topic']
)

#### 2nd prompt - summarizer prompt
prompt2 = PromptTemplate(
        template='Generate a 5 pointer summary from the following \n {text}',
        input_variables=['text']
)


#### 2 model - for report and summary
model = ChatOpenAI(
    model="gpt-4o-2024-08-06",
)

#### 3 parser for both
parser = StrOutputParser()



#### chain(LCEL)

chain = prompt1 | model | parser | prompt2 | model | parser

config = {
    'run_name' : 'Custom name TBD',
    'tags':['complex llm app', 'report generation'],
    'metadata' : {'model1' : 'gpt 4o', 'model2': 'gpt 4o'}
}


result = chain.invoke({'topic': 'India'}, config=config)

print(result)

print(chain.get_graph().print_ascii())