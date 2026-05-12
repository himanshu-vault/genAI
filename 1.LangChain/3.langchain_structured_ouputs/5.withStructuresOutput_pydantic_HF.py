from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal


llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation"
)

model = ChatHuggingFace(model=llm)


class Review(BaseModel):
    key_themes: list[str] = Field(description="major theme about which review is written")
    summary:    str = Field(description="A brief summary of the review")
    sentiment:  Literal['Pos', 'Neg', 'Neut'] = Field(description="return review sentiment - positive, negative or neutral")
    pros:       Optional[list[str]] = Field(default=None, description="Write all pros inside a list")
    cons:       Optional[list[str]] = Field(default=None, description="Write all cons inside a list")
    name:       Optional[str] = Field(description="Write the name of the reviewer")


structured_model = model.with_structured_output(Review)

review1 = """       
            The hardware is great, but the software feels bloated. 
            There are too many pre-installed apps that I can't remove. 
            Also, the UI looks outdated compared to other brands. 
            Hoping for a software update to fix this."""


review2 = """
    I recently upgraded to Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3    the processor makes everything
    lightning fast—whether I'm gaming, multitasking, or editing photos. The 5ØeemAh battery easily
    heavy use, and the 45W fast charging is a lifesaver.
    lasts full day even with

    The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really     blew me
    away with the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in Iow light. Zooming up    to leøx
    actually works well for distant objects, but anything beyond 30x loses quality.

    However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with
    bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also    a hard
    pill to swallow.

    pros :
    Insanely powerful processor (great for gaming and productivity)
    Stunning 200MP camera with incredible zoom capabilities
    Long battery life with fast charging
    S-Pen support is unique and useful

    Cons :
    Bulky and heavy—not great for one-handed use
    Bloatware still exists in One UI
    Expensive compared to competitors
"""

# result = structured_model.invoke(review1)
result = structured_model.invoke(review2)



print("--------------------type(result)  >",type(result))
print("--------------------result        >",result)


result = dict(result)

print("--------------------Summary       >",result['summary'])
print("--------------------sentiment     >",result['sentiment'])

# print while using review 2
print("--------------------key_themes    >",result['key_themes'])
print("--------------------pros          >",result['pros'])
print("--------------------cons          >",result['cons'])
print("--------------------reviewer_name >",result.get('name'))
