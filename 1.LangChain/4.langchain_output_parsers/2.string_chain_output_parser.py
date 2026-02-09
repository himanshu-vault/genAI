from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
    )

model = ChatHuggingFace(llm=llm)



#1st prompt - detailed report of a topic
template1 = PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=['topic']
)


#2nd prompt - summary of the detailed report
template2 = PromptTemplate(
    template="write a 5 line summary on the following {text}",
    input_variables=['text']
)

##############################    NOT NEEDED    ###################################
# prompt1 = template1.invoke({'topic':'Black Hole'})
# result = model.invoke(prompt1)

# prompt2 = template2.invoke({'text':result.content})
# result1 = model.invoke(prompt2)

# print(result1.content)
###################################################################################

parser = StrOutputParser()

# Chain :)
chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic': "Black Hole"})

print(result)