from graders.base import BaseGrader


class MediumGrader(BaseGrader):
    def grade(self, trajectory, ground_truth) -> float:
        expected_sequence = ground_truth["sequence"]

        score = 0.0
        matched = 0

        for i, step in enumerate(trajectory):
            if i >= len(expected_sequence):
                break

            action = step["action"]
            expected = expected_sequence[i]

            if action["type"] == expected["type"]:
                matched += 1

        score = matched / len(expected_sequence)
        return score