from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel


# two parallel runnables
# runnable 1 - tweet generator
# runnable 2 - linkedin post generator


prompt1 = PromptTemplate(
    template="Generate a tweet about a {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Generate a linkedIN post about \n {topic}",
    input_variables=['topic']
)

#model
model = ChatOpenAI()

#parser
parser = StrOutputParser()

# 2 sequential chain whch will run parallely
chain1 = RunnableSequence(prompt1, model, parser)
chain2 = RunnableSequence(prompt2, model, parser)

# running above chains parallely
parallel_chain = RunnableParallel({
    'tweet':chain1,
    'linkedin':chain2
    })
    
    
#invoking
result = parallel_chain.invoke({'topic':'AI'})

print("['tweet - ", result['tweet'])
print("['linkedin - ", result['linkedin'])