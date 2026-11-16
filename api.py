from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Reformer Class Planner is running!"}