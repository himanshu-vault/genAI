# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}