from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough

### sequentially generating joke and explanation, hides joke in the chain and becomes invisible

### sequential chain to create joke

### 2 parallel chains 
### 1 - passthrough chain - to passthrough joke as it is
### 2 - explainer chain   -  runs parallel to passthough 
### both of above gets same input from the create joke chain

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

joke_gen = RunnableSequence(prompt1, model, parser)

parallel_chain = RunnableParallel(
    {
    'joke':        RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, model, parser)
    }
)

final_chain = RunnableSequence(joke_gen, parallel_chain)

result = final_chain.invoke({'topic':'AI'})

print(result)