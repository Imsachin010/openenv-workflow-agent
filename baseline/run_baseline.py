from tasks.easy import create_easy_task
from tasks.medium import create_medium_task
from tasks.hard import create_hard_task

from graders.easy_grader import EasyGrader
from graders.medium_grader import MediumGrader
from graders.hard_grader import HardGrader

from app.env import WorkflowEnv
from baseline.policy import BaselinePolicy


def run_task(task_name, create_task_fn, grader_cls):
    state, ground_truth = create_task_fn()
    env = WorkflowEnv(state)
    policy = BaselinePolicy()

    obs = env.reset()

    done = False
    steps = 0

    while not done and steps < 10:
        action = policy.act(obs)

        if action is None:
            break

        obs, reward, done, _ = env.step(action)
        steps += 1

    trajectory = env.state().history
    print(f"{task_name} trajectory:", trajectory)

    grader = grader_cls()
    score = grader.grade(trajectory, ground_truth)

    return score


def main():
    results = {}

    results["easy"] = run_task("easy", create_easy_task, EasyGrader)
    results["medium"] = run_task("medium", create_medium_task, MediumGrader)
    results["hard"] = run_task("hard", create_hard_task, HardGrader)

    print("\n===== BASELINE RESULTS =====")
    for k, v in results.items():
        print(f"{k}: {round(v, 3)}")


if __name__ == "__main__":
    main()