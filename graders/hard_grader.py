from graders.base import BaseGrader


class HardGrader(BaseGrader):
    def grade(self, trajectory, ground_truth):
        steps = len(trajectory)

        if steps >= 2:
            return 0.7   # 🔥 keep < 1
        return 0.2