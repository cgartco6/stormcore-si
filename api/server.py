from fastapi import FastAPI
from pydantic import BaseModel
from core.runtime.engine import StormCoreEngine

app = FastAPI()
engine = StormCoreEngine()
engine.boot()


class RepoRequest(BaseModel):
    repo_path: str


@app.get("/")
def home():
    return {"status": "StormCore Online"}


@app.post("/complete")
async def complete_repo(request: RepoRequest):
    result = await engine.complete_repository(request.repo_path)
    return result
