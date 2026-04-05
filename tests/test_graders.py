from tasks.easy import create_easy_task
from app.env import WorkflowEnv
from app.actions import Action
from graders.easy_grader import EasyGrader

state, gt = create_easy_task()
env = WorkflowEnv(state)

obs = env.reset()

# Correct action
action = Action(type="classify", target_id="1", payload={"label": "meeting_request"})
env.step(action)

trajectory = env.state().history

grader = EasyGrader()
score = grader.grade(trajectory, gt)

print("Score:", score)