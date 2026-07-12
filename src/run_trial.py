from __future__ import annotations

from typing import Any
from psyflow import StimUnit, next_trial_id, set_trial_context
from .utils import TrialPlan


def _squares(stim_bank, colors: list[str], positions: list[list[float]], size: float) -> list[Any]:
    return [stim_bank.rebuild("color_square", fillColor=color, lineColor=color, pos=pos, width=size, height=size)
            for color, pos in zip(colors, positions)]


def _context(unit, *, trial_id: int, block_id: str, plan: dict[str, Any], phase: str,
             deadline: float, keys: list[str], stim_id: str) -> None:
    set_trial_context(unit, trial_id=trial_id, phase=phase, deadline_s=deadline, valid_keys=keys,
                      block_id=block_id, condition_id=plan["condition_id"],
                      task_factors={**plan, "stage": phase}, stim_id=stim_id)


def run_trial(win, kb, settings, condition, stim_bank, trigger_runtime, block_id=None, block_idx=None):
    if not isinstance(condition, TrialPlan): raise TypeError("Change detection requires a preplanned TrialPlan")
    plan = condition.to_dict(); trial_id = next_trial_id(); block_name = str(block_id or "scored")
    data: dict[str, Any] = {"trial_id": trial_id, "phase": "test_array", "block_id": block_name,
                            "block_idx": int(block_idx or 0), **plan}
    fixation = StimUnit("fixation", win, kb, runtime=trigger_runtime).add_stim(stim_bank.get("fixation"))
    _context(fixation, trial_id=trial_id, block_id=block_name, plan=plan, phase="fixation",
             deadline=float(settings.fixation_duration), keys=[], stim_id="fixation")
    fixation.show(duration=float(settings.fixation_duration), onset_trigger=settings.triggers.get("fixation")).to_dict(data)
    memory = StimUnit("memory_array", win, kb, runtime=trigger_runtime).add_stim(*_squares(stim_bank, plan["memory_colors"], plan["positions"], float(settings.square_size_deg)))
    _context(memory, trial_id=trial_id, block_id=block_name, plan=plan, phase="memory_array",
             deadline=float(settings.memory_duration), keys=[], stim_id=f"memory_set_{plan['set_size']}")
    memory.show(duration=float(settings.memory_duration), onset_trigger=settings.triggers.get(f"memory_set_{plan['set_size']}")).to_dict(data)
    delay = StimUnit("retention", win, kb, runtime=trigger_runtime).add_stim(stim_bank.get("fixation"))
    _context(delay, trial_id=trial_id, block_id=block_name, plan=plan, phase="retention",
             deadline=float(settings.retention_duration), keys=[], stim_id="retention_fixation")
    delay.show(duration=float(settings.retention_duration), onset_trigger=settings.triggers.get("retention")).to_dict(data)
    keys = ["f", "j"]
    test = StimUnit("test_array", win, kb, runtime=trigger_runtime).add_stim(*_squares(stim_bank, plan["test_colors"], plan["positions"], float(settings.square_size_deg)))
    _context(test, trial_id=trial_id, block_id=block_name, plan=plan, phase="test_array",
             deadline=float(settings.response_window), keys=keys, stim_id=f"test_{plan['change_status']}_set_{plan['set_size']}")
    test.capture_response(keys=keys, correct_keys=[plan["correct_key"]], duration=float(settings.response_window),
                          onset_trigger=settings.triggers.get(f"test_{plan['change_status']}"),
                          response_trigger={"f": settings.triggers.get("same_response"), "j": settings.triggers.get("change_response")},
                          timeout_trigger=settings.triggers.get("response_timeout"), terminate_on_response=True).to_dict(data)
    response = test.get_state("response", None); correct = response == plan["correct_key"]
    if response is None: outcome = "timeout"
    elif plan["change_status"] == "change": outcome = "hit" if response == "j" else "miss"
    else: outcome = "false_alarm" if response == "j" else "correct_rejection"
    data.update(response_key=str(response or ""), response_rt=test.get_state("rt", None), correct=correct, outcome=outcome)
    return data
