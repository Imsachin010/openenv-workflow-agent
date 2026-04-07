from graders.base import BaseGrader


class MediumGrader(BaseGrader):
    def grade(self, trajectory, ground_truth):
        if len(trajectory) > 1:
            return 0.6
        return 0.2