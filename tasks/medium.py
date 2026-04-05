from app.state import EnvironmentState, Email, HiddenEmailState


def create_medium_task():
    email = Email(
        id="1",
        sender="client@company.com",
        subject="Project Update",
        body="Please send the latest report and confirm timeline"
    )

    hidden = HiddenEmailState(
        email_id="1",
        true_intent="task_request",
        urgency="medium",
        requires_response=True,
        deadline=6,
        missing_information=False
    )

    state = EnvironmentState(
        emails=[email],
        tasks=[],
        calendar=[],
        hidden_email_states=[hidden]
    )

    ground_truth = {
        "sequence": [
            {"type": "classify", "label": "task_request"},
            {"type": "reply"}
        ]
    }

    return state, ground_truth