from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


###### objective

# parallel chain needed to process one document
#  > LLM1 > 1 Summary
#  > LLM2 > 2 Quiz

# output from LLM1 and LLM2 will merge together into one doc using LLM 




#### 1st prompt - detailed report
prompt1 = PromptTemplate(
        template='Generate short and simple notes from the text - \n {text}',
        input_variables=['text']
)



#### 2nd prompt - quiz prompt
prompt2 = PromptTemplate(
        template='from the following text \n {text} \n Generate 5 short question and answers',
        input_variables=['text']
)


#### 3rd prompt - summarizer prompt
prompt3 = PromptTemplate(
        template='Merge the provided notes and quiz into one single document \n {notes} \n {quiz} ',
        input_variables=['notes', 'quiz']
)



#### 1st model - for report & merge
model1 = ChatOpenAI()

#### 2nd model - for Quiz
model2 = ChatAnthropic(model_name="claude-3-7-sonnet-20250219")

#### 3 parser for both
parser = StrOutputParser()



#### parallel chain(LCEL)
chains = {
        'notes' : prompt1 | model1 | parser,
        'quiz' : prompt2 | model2 | parser
        }

parallel_chains = RunnableParallel(chains)

#### merge Chain into one
merge_chain = prompt3 | model1 | parser

#### final chain - parallel chains getting connected to merge chain
chain = parallel_chains | merge_chain

### reading file data to provide model input
data = open(r'D:\local_synced\workspace\genAI\1.LangChain\5.Chains\intro_ds.txt').read()

#### invoke chain
result = chain.invoke({'text':'Data Science'})

print(result)
print(chain.get_graph().print_ascii())