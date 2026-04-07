from graders.base import BaseGrader


class EasyGrader(BaseGrader):
    def grade(self, trajectory, ground_truth):
        # simple logic
        if len(trajectory) > 0:
            return 0.95   # 🔥 NOT 1.0
        return 0.1