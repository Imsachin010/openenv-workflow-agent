from app.state import EnvironmentState, Email, HiddenEmailState


def create_hard_task():
    email = Email(
        id="1",
        sender="manager@company.com",
        subject="Catch up",
        body="Let's meet sometime next week"
    )

    hidden = HiddenEmailState(
        email_id="1",
        true_intent="meeting_request",
        urgency="medium",
        requires_response=True,
        deadline=8,
        missing_information=True
    )

    state = EnvironmentState(
        emails=[email],
        tasks=[],
        calendar=[],
        hidden_email_states=[hidden]
    )

    ground_truth = {
        "sequence": [
            {"type": "request_info"},
            {"type": "classify", "label": "meeting_request"},
            {"type": "schedule"}
        ]
    }

    return state, ground_truth