from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
    )

model = ChatHuggingFace(llm=llm)


parser = JsonOutputParser()

#1st prompt - detailed report of a topic
template = PromptTemplate(
    template="Give me the name , age, city of a fictional person \n {format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

# prompt = template.format()
# print("prompt - ", prompt)

# result = model.invoke(prompt)
# print("result -", result) 

# final_result = parser.parse(result.content)
# print("final_result - ", final_result)

chain = template | model | parser
result = chain.invoke({})
print(result)