from graders.base import BaseGrader


class EasyGrader(BaseGrader):
    def grade(self, trajectory, ground_truth) -> float:
        correct_label = ground_truth["label"]

        for step in trajectory:
            action = step["action"]

            if action["type"] == "classify":
                if action.get("payload", {}).get("label") == correct_label:
                    return 1.0
                else:
                    return 0.0

        return 0.0