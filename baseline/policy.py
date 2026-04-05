from app.actions import Action


class BaselinePolicy:
    def act(self, observation):
        if not observation.emails:
            return None

        email = observation.emails[0]
        text = (email.subject + " " + email.body).lower()

        # Heuristic rules
        if "meet" in text:
            return Action(
                type="classify",
                target_id=email.id,
                payload={"label": "meeting_request"}
            )

        elif "report" in text or "update" in text:
            return Action(
                type="classify",
                target_id=email.id,
                payload={"label": "task_request"}
            )

        return Action(
            type="archive",
            target_id=email.id
        )