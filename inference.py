import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from app.env import WorkflowEnv
from app.actions import Action
from tasks.hard import create_hard_task
from graders.hard_grader import HardGrader
# ---------------- ENV CONFIG ----------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


# ---------------- LOGGING ----------------
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ---------------- SIMPLE POLICY ----------------
def get_action(obs):
    if not obs.emails:
        return None

    email = obs.emails[0]

    # 🔥 IMPORTANT: detect if we already asked info
    already_asked = any(
        h["action"]["type"] == "request_info"
        for h in obs.history
    )

    text = (email.subject + " " + email.body).lower()

    # If info already requested → do NOT ask again
    if already_asked:
        return Action(
            type="classify",
            target_id=email.id,
            payload={"label": "meeting_request"}
        )

    # First step: ask info if ambiguous
    if "sometime" in text or "next week" in text:
        return Action(type="request_info", target_id=email.id)

    return Action(type="archive", target_id=email.id)


# ---------------- MAIN ----------------
def main():
    state, gt = create_hard_task()
    env = WorkflowEnv(state)
    grader = HardGrader()

    obs = env.reset()

    rewards = []
    steps = 0

    log_start("hard", "workflow-env", MODEL_NAME)

    try:
        done = False

        while not done and steps < 10:
            action = get_action(obs)
            if action is None:
                break

            obs, reward, done, _ = env.step(action)

            rewards.append(reward)
            steps += 1

            log_step(steps, action.type, reward, done, None)

            # 🔥 STOP CONDITION (IMPORTANT)
            if action.type == "classify":
                break

        trajectory = env.state().history
        score = grader.grade(trajectory, gt)

        score = max(0.0, min(1.0, score))

        success = score > 0.3

    finally:
        log_end(success, steps, score, rewards)


if __name__ == "__main__":
    main()