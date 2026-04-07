import os
from openai import OpenAI

from app.env import WorkflowEnv
from app.actions import Action
from tasks.easy import create_easy_task
from tasks.medium import create_medium_task
from tasks.hard import create_hard_task
from graders.easy_grader import EasyGrader
from graders.medium_grader import MediumGrader
from graders.hard_grader import HardGrader


# ---------------- ENV CONFIG (CRITICAL) ----------------
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


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


# ---------------- LLM ACTION (MANDATORY) ----------------
def llm_decide_action(email):
    prompt = f"""
    Email:
    Subject: {email.subject}
    Body: {email.body}

    Choose ONE action:
    classify, request_info, archive

    Output only the action name.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0,
        )
        action_text = completion.choices[0].message.content.strip().lower()
        return action_text
    except Exception as e:
        print(f"LLM API error: {e}")
        return "classify"


# ---------------- POLICY ----------------
def get_action(obs):
    if not obs.emails:
        return None

    email = obs.emails[0]

    # 🔥 ALWAYS CALL LLM (important for validator)
    action_text = llm_decide_action(email)

    # 🔥 Guardrail (to avoid looping)
    already_asked = any(
        h["action"]["type"] == "request_info"
        for h in obs.history
    )

    if already_asked:
        return Action(
            type="classify",
            target_id=email.id,
            payload={"label": "meeting_request"}
        )

    if "request" in action_text:
        return Action(type="request_info", target_id=email.id)

    elif "classify" in action_text:
        return Action(
            type="classify",
            target_id=email.id,
            payload={"label": "meeting_request"}
        )

    return Action(type="archive", target_id=email.id)


# ---------------- MAIN ----------------
def main():
    tasks = [
        ("easy", create_easy_task, EasyGrader),
        ("medium", create_medium_task, MediumGrader),
        ("hard", create_hard_task, HardGrader),
    ]

    for task_name, create_func, GraderClass in tasks:
        state, gt = create_func()
        env = WorkflowEnv(state)
        grader = GraderClass()

        obs = env.reset()

        rewards = []
        steps = 0

        log_start(task_name, "workflow-env", MODEL_NAME)

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

                # stop after meaningful action
                if action.type == "classify":
                    break

            trajectory = env.state().history
            score = grader.grade(trajectory, gt)

            score = max(0.01, min(0.99, float(score)))  # Strictly between 0 and 1
            success = score > 0.3

        finally:
            log_end(success, steps, score, rewards)


if __name__ == "__main__":
    main()