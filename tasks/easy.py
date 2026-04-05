from app.state import EnvironmentState, Email, HiddenEmailState


def create_easy_task():
    email = Email(
        id="1",
        sender="boss@company.com",
        subject="Team Meeting",
        body="Schedule a meeting tomorrow at 10am"
    )

    hidden = HiddenEmailState(
        email_id="1",
        true_intent="meeting_request",
        urgency="high",
        requires_response=True,
        deadline=5,
        missing_information=False
    )

    state = EnvironmentState(
        emails=[email],
        tasks=[],
        calendar=[],
        hidden_email_states=[hidden]
    )

    ground_truth = {
        "correct_action": "classify",
        "label": "meeting_request"
    }

    return state, ground_truth