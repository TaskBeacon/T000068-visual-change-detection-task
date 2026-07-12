from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo

@dataclass
class TaskSamplerResponder:
    continue_key: str = "space"
    accuracy_by_set_size: dict[int, float] = field(default_factory=lambda: {2: .98, 4: .90, 6: .78, 8: .68})
    rt_s: float = .45
    forced_error_trials: list[int] = field(default_factory=list)
    forced_timeout_trials: list[int] = field(default_factory=list)
    def __post_init__(self): self.rng: Any = None
    def start_session(self, session: SessionInfo, rng: Any): self.rng = rng
    def on_feedback(self, fb: Feedback): return None
    def end_session(self): self.rng = None
    def act(self, obs: Observation) -> Action:
        keys = [str(k) for k in (obs.valid_keys or [])]
        if not keys: return Action(key=None, rt_s=None)
        factors = dict(getattr(obs, "task_factors", {}) or {}); stage = str(factors.get("stage", getattr(obs, "phase", "")))
        if stage in {"instruction", "practice_summary", "good_bye"}: return Action(key=self.continue_key if self.continue_key in keys else keys[0], rt_s=.05)
        if stage != "test_array": return Action(key=None, rt_s=None)
        trial_id = int(getattr(obs, "trial_id", -1)) if str(getattr(obs, "trial_id", "")).isdigit() else -1
        if trial_id in self.forced_timeout_trials: return Action(key=None, rt_s=None)
        correct = str(factors.get("correct_key", "f")); rate = self.accuracy_by_set_size.get(int(factors.get("set_size", 4)), .8)
        draw = float(self.rng.random()) if hasattr(self.rng, "random") else .5
        choose_correct = trial_id not in self.forced_error_trials and draw <= rate
        key = correct if choose_correct else next((k for k in keys if k != correct), keys[0])
        return Action(key=key, rt_s=self.rt_s)

