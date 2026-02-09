from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


#### model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
    )
model = ChatHuggingFace(llm=llm)



#### Pydantic object

class Person(BaseModel):
    name: str = Field(description='Name of a person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of City of the person')


parser = PydanticOutputParser(pydantic_object=Person)


#1st prompt - detailed report of a topic
template = PromptTemplate(
    template="Give me name, age and city of a fictional {place} \n {format_instruction}",
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

#### synthesizing prompt
prompt = template.invoke({'place':'Indian'})
print("prompt - ", prompt)

#### chain
chain = template | model | parser
result = chain.invoke({'place':'Indian'})
print(result)