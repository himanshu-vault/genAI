from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

### sequential chain
### generate the joke > explain the joke

prompt1 = PromptTemplate(
    template="Write a joke about a {topic}",
    input_variables=['topic']
)


prompt2 = PromptTemplate(
    template="Explain the following joke \n {text}",
    input_variables=['text']
)

model = ChatOpenAI()

parser = StrOutputParser()

chain = RunnableSequence(prompt1, model, parser, prompt2, model, parser)


result = chain.invoke({'topic':'AI'})

print(result)