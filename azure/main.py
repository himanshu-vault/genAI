from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Azure OpenAI client

# from openai import OpenAI
# client = OpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT')}openai/deployments/{os.getenv('AZURE_OPENAI_DEPLOYMENT')}",
# )

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# Define request structure
class QuestionRequest(BaseModel):
    question: str

# Define the API endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.question}
            ]
        )
        answer = response.choices[0].message.content
        return {"question": request.question, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
def root():
    return {"status": "running"}