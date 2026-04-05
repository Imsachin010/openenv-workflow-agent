class BaseGrader:
    def grade(self, trajectory, ground_truth) -> float:
        raise NotImplementedError