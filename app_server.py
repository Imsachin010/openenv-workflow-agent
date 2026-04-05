from fastapi import FastAPI
from app.env import WorkflowEnv
from tasks.easy import create_easy_task

app = FastAPI()


@app.post("/reset")
def reset():
    state, _ = create_easy_task()
    env = WorkflowEnv(state)
    obs = env.reset()

    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Workflow Env is running"}
    
@app.get("/")
def home():
    return {"message": "Workflow Env API running"}