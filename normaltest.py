from tasks.easy import create_easy_task
from app.env import WorkflowEnv
from app.actions import Action

state, gt = create_easy_task()
env = WorkflowEnv(state)

obs = env.reset()
print("Initial:", obs)

# Try correct classify
action = Action(
    type="classify",
    target_id="1",
    payload={"label": "meeting_request"}
)

obs, reward, done, _ = env.step(action)

print("After step:", obs)
print("Reward:", reward)