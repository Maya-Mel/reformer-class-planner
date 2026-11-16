from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class ClassRequest(BaseModel):
    request: str

@app.get("/")
def home():
    return {"message": "Reformer Class Planner is running!"}

@app.post("/class")
def build_class(class_request: ClassRequest):
    lesson = run_agent(class_request.request)
    return {"lesson": lesson}