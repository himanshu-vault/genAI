from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda, RunnableBranch

#### runnable branch - langchains if else
#### call different chains based on a decision



#### A complaint comes in -
#### LLM decides a category
#### only a specific branch will run based on the category



prompt1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)



prompt2 = PromptTemplate(
    template="Summarize the following {text}",
    input_variables=['text']
)


model = ChatOpenAI()

parser = StrOutputParser()

report_generation_chain = RunnableSequence(prompt1, model, parser)

branch_chain = RunnableBranch(
    (lambda x : len(x.split())>500, RunnableSequence(prompt2, model, parser)),  #### condition1
    RunnablePassthrough()     #### default condition
)


final_chain = RunnableSequence(report_generation_chain, branch_chain)

# result = final_chain.invoke({'topic':'AI vs genAI'})

result = final_chain.invoke({'topic':'Russia vs Ukraine'})

print(result)