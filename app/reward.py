from app.state import EnvironmentState


def compute_reward(state: EnvironmentState, action_type: str, info: dict) -> float:
    reward = 0.0

    # --- Correctness ---
    if info.get("correct_action"):
        reward += 0.2

    # Cost for asking info (tradeoff)
    if action_type == "request_info":
        reward -= 0.05  # cost for querying
    elif info.get("incorrect_action"):
        reward -= 0.2

    # --- Progress ---
    if info.get("task_progress"):
        reward += 0.2

    # --- Step penalty (efficiency)
    reward -= 0.01

    # --- Deadline penalty ---
    for hidden in state.hidden_email_states:
        if hidden.deadline and state.timestep > hidden.deadline:
            reward -= 0.5

    return reward