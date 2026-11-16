from fastapi import FastAPI, HTTPException
from tools import KNOWN_LEVELS, validate_conditions
from pydantic import BaseModel
from agent import run_agent
from fastapi.responses import FileResponse

app = FastAPI()

class ClassRequest(BaseModel):
    level: str
    conditions: list[str] = []
    focus_areas: list[str] = []

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/class")
def build_class(class_request: ClassRequest):
    if class_request.level not in KNOWN_LEVELS:
        raise HTTPException(status_code=400, detail=f"Unknown level: {class_request.level}. Use one of: {', '.join(KNOWN_LEVELS)}")
    try:
        validate_conditions(class_request.conditions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    request = f"Build a 50 minute {class_request.level} reformer class."

    if class_request.conditions:
        request += f" The client has these conditions: {', '.join(class_request.conditions)}."

    if class_request.focus_areas:
        request += f" Focus on these areas: {', '.join(class_request.focus_areas)}."

    lesson = run_agent(request)
    return {"lesson": lesson}