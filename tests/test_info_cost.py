from tasks.hard import create_hard_task
from app.env import WorkflowEnv
from app.actions import Action


def test_info_cost():
    # ------------------------
    # CASE 1: WITH info
    # ------------------------
    state, _ = create_hard_task()
    env = WorkflowEnv(state)

    obs = env.reset()

    action = Action(type="request_info", target_id="1")
    obs, r1, _, _ = env.step(action)

    action = Action(type="classify", target_id="1", payload={"label": "meeting_request"})
    obs, r2, _, _ = env.step(action)

    print("\nWITH INFO:")
    print("request_info:", r1)
    print("classify:", r2)

    # ------------------------
    # CASE 2: WITHOUT info
    # ------------------------
    state2, _ = create_hard_task()
    env2 = WorkflowEnv(state2)

    obs = env2.reset()

    action = Action(type="classify", target_id="1", payload={"label": "meeting_request"})
    obs, r_direct, _, _ = env2.step(action)

    print("\nWITHOUT INFO:")
    print("direct classify:", r_direct)


if __name__ == "__main__":
    test_info_cost()