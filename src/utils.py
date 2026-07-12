from __future__ import annotations

import hashlib
import random
from typing import Any

SET_SIZES = (2, 4, 6, 8)
POSITIONS = ((-4.5, 2.8), (0.0, 2.8), (4.5, 2.8), (-4.5, 0.0), (4.5, 0.0), (-4.5, -2.8), (0.0, -2.8), (4.5, -2.8))
COLORS = ("#e63946", "#ff9f1c", "#f6d743", "#2a9d8f", "#00b4d8", "#4361ee", "#9b5de5", "#f15bb5", "#90be6d")


class TrialPlan(str):
    def __new__(cls, *, set_size: int, change_status: str, memory_colors: list[str],
                test_colors: list[str], positions: list[tuple[float, float]], changed_index: int | None,
                is_practice: bool, trial_index_in_block: int) -> "TrialPlan":
        condition = f"set_{set_size}_{change_status}"
        obj = str.__new__(cls, condition)
        obj.set_size = int(set_size); obj.change_status = change_status
        obj.memory_colors = list(memory_colors); obj.test_colors = list(test_colors)
        obj.positions = [tuple(p) for p in positions]; obj.changed_index = changed_index
        obj.is_practice = bool(is_practice); obj.trial_index_in_block = int(trial_index_in_block)
        return obj

    def to_dict(self) -> dict[str, Any]:
        return {"condition": str(self), "condition_id": str(self), "set_size": self.set_size,
                "change_status": self.change_status, "memory_colors": self.memory_colors,
                "test_colors": self.test_colors, "positions": [list(p) for p in self.positions],
                "changed_index": self.changed_index, "is_practice": self.is_practice,
                "trial_index_in_block": self.trial_index_in_block,
                "correct_key": "j" if self.change_status == "change" else "f"}


def _seed(base: int, label: str) -> int:
    return int.from_bytes(hashlib.blake2b(f"{base}|change-detection|{label}".encode(), digest_size=8).digest(), "big")


def generate_trial_plans(*, repetitions_per_cell: int, seed: int, is_practice: bool) -> list[TrialPlan]:
    rng = random.Random(_seed(seed, "practice" if is_practice else "scored"))
    raw: list[dict[str, Any]] = []
    for set_size in SET_SIZES:
        for change_status in ("same", "change"):
            for _ in range(int(repetitions_per_cell)):
                positions = rng.sample(list(POSITIONS), set_size)
                memory = rng.sample(list(COLORS), set_size)
                test = list(memory); changed_index = None
                if change_status == "change":
                    changed_index = rng.randrange(set_size)
                    choices = [color for color in COLORS if color not in memory]
                    test[changed_index] = rng.choice(choices)
                raw.append({"set_size": set_size, "change_status": change_status,
                            "memory_colors": memory, "test_colors": test,
                            "positions": positions, "changed_index": changed_index})
    rng.shuffle(raw)
    return [TrialPlan(**item, is_practice=is_practice, trial_index_in_block=i) for i, item in enumerate(raw)]


def summarize_trials(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [row for row in rows if not bool(row.get("is_practice"))]
    result: dict[str, Any] = {"accuracy": sum(bool(r.get("correct")) for r in scored) / len(scored) if scored else 0.0}
    k_values: list[float] = []
    for size in SET_SIZES:
        changed = [r for r in scored if int(r.get("set_size", 0)) == size and r.get("change_status") == "change"]
        same = [r for r in scored if int(r.get("set_size", 0)) == size and r.get("change_status") == "same"]
        hit = sum(r.get("outcome") == "hit" for r in changed) / len(changed) if changed else 0.0
        false_alarm = sum(r.get("outcome") == "false_alarm" for r in same) / len(same) if same else 0.0
        k = size * (hit - false_alarm)
        result[f"set_{size}_hit_rate"] = hit; result[f"set_{size}_false_alarm_rate"] = false_alarm; result[f"set_{size}_k"] = k
        k_values.append(k)
    result["max_k"] = max(k_values) if k_values else 0.0
    return result

