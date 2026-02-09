from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda

#### runnable lambda converts regular python function into langchain runnable
#### so that regular python function can be used in the chains



# runnable lambda demo - 
# def word_count(joke):
#     return(len(joke.split()))

# word_counter = RunnableLambda(word_count)
# print(word_counter.invoke('This is a joke'))
# exit()

#### joke gen (llm)
#### count number of words in the joke (python function)

prompt1 = PromptTemplate(
    template="Write a joke about a {topic}",
    input_variables=['topic']
)

model = ChatOpenAI()

parser = StrOutputParser()

joke_gen = RunnableSequence(prompt1, model, parser)

def word_count(joke):
    return(len(joke.split()))


parallel_chain = RunnableParallel(
    {
    'joke':  RunnablePassthrough(),
    'count': RunnableLambda(word_count)
    }
)

final_chain = RunnableSequence(joke_gen, parallel_chain)

result = final_chain.invoke({'topic':'AI'})

print("joke - ", result['joke'])
print("count - ", result['count'])