from app.state import EnvironmentState


def apply_action(state: EnvironmentState, action):
    info = {
        "correct_action": False,
        "incorrect_action": False,
        "task_progress": False
    }

    # Find hidden truth
    hidden = next(
        (h for h in state.hidden_email_states if h.email_id == action.target_id),
        None
    )
    # ----------------------------
    # CLASSIFY
    # ----------------------------
    # if action.type == "classify":
    #     predicted = action.payload.get("label") if action.payload else None

    #     if hidden:
    #         # 🔥 NEW: penalize guessing under uncertainty
    #         if hidden.missing_information:
    #             info["incorrect_action"] = True  # cannot classify correctly without info

    #     elif predicted == hidden.true_intent:
    #         info["correct_action"] = True
    #         info["task_progress"] = True

    #     else:
    #         info["incorrect_action"] = True
    if action.type == "classify":
        predicted = action.payload.get("label") if action.payload else None

        if not hidden:
            info["incorrect_action"] = True

        elif hidden.missing_information:
            # ❌ Cannot classify without info
            info["incorrect_action"] = True

        else:
            # ✅ Now classification is allowed
            if predicted == hidden.true_intent:
                info["correct_action"] = True
                info["task_progress"] = True
            else:
                info["incorrect_action"] = True
    # ----------------------------
    # ARCHIVE
    # ----------------------------
    elif action.type == "archive":
        state.emails = [e for e in state.emails if e.id != action.target_id]
        info["task_progress"] = True

    # ----------------------------
    # REQUEST INFO
    # ----------------------------
    elif action.type == "request_info":
        if hidden and hidden.missing_information:
            hidden.missing_information = False
            info["correct_action"] = True
        else:
            info["incorrect_action"] = True

    # ----------------------------
    # REPLY
    # ----------------------------
    elif action.type == "reply":
        if hidden and hidden.requires_response:
            hidden.requires_response = False
            info["correct_action"] = True
        else:
            info["incorrect_action"] = True

    return state, info