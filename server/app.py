from fastapi import FastAPI
from app.env import WorkflowEnv
from tasks.easy import create_easy_task

app = FastAPI()


@app.post("/reset")
def reset():
    state, _ = create_easy_task()
    env = WorkflowEnv(state)
    env.reset()
    return {"status": "ok"}


@app.get("/")
def home():
    return {"message": "Workflow Env is running"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()