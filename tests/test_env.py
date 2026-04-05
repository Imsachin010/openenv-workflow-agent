from app.env import WorkflowEnv
from app.state import EnvironmentState, Email, HiddenEmailState

initial_state = EnvironmentState(
    emails=[
        Email(id="1", sender="boss@company.com", subject="Meeting", body="Let's meet")
    ],
    tasks=[],
    calendar=[],
    hidden_email_states=[
        HiddenEmailState(
            email_id="1",
            true_intent="meeting_request",
            urgency="high",
            requires_response=True,
            deadline=5,
            missing_information=True
        )
    ]
)

env = WorkflowEnv(initial_state)

obs = env.reset()
print(obs)

from app.actions import Action
obs, reward, done, _ = env.step(Action(type="archive", target_id="1"))

print(obs, reward, done)