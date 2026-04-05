from typing import Tuple, Dict, Any
from copy import deepcopy

from .state import EnvironmentState
from .observation import Observation
from .actions import Action
from .transition import apply_action
from .reward import compute_reward


class WorkflowEnv:
    def __init__(self, initial_state: EnvironmentState):
        self.initial_state = deepcopy(initial_state)
        self._state = deepcopy(initial_state)

    # -----------------------------
    # RESET
    # -----------------------------
    def reset(self) -> Observation:
        self._state = deepcopy(self.initial_state)
        return self._get_observation()

    # -----------------------------
    # STEP
    # -----------------------------
    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self._state.done:
            raise Exception("Episode already finished. Call reset().")

        # Log action
        self._state.history.append({
            "timestep": self._state.timestep,
            "action": action.model_dump()
        })

        # ✅ APPLY TRANSITION (NEW)
        self._state, info = apply_action(self._state, action)

        # ✅ COMPUTE REWARD (NEW)
        reward = compute_reward(self._state, action.type, info)

        # Increment timestep
        self._state.timestep += 1

        # Episode termination
        if self._state.timestep >= 10:
            self._state.done = True

        return self._get_observation(), reward, self._state.done, {}

    # -----------------------------
    # STATE ACCESS
    # -----------------------------
    def state(self) -> EnvironmentState:
        return self._state

    # -----------------------------
    # OBSERVATION
    # -----------------------------
    def _get_observation(self) -> Observation:
        return Observation(
            emails=self._state.emails,
            tasks=self._state.tasks,
            calendar=self._state.calendar,
            history=self._state.history,
            timestep=self._state.timestep
        )