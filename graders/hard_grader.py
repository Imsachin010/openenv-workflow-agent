from graders.base import BaseGrader


class HardGrader(BaseGrader):
    def grade(self, trajectory, ground_truth) -> float:
        expected_sequence = ground_truth["sequence"]

        matched = 0
        penalty = 0

        for i, step in enumerate(trajectory):
            if i >= len(expected_sequence):
                break

            action = step["action"]
            expected = expected_sequence[i]

            if action["type"] == expected["type"]:
                matched += 1
            else:
                penalty += 1

        score = matched / len(expected_sequence)
        score -= 0.1 * penalty

        return max(0.0, min(1.0, score))