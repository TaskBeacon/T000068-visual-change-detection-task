from __future__ import annotations
from contextlib import nullcontext
from functools import partial
from pathlib import Path
from typing import Any
import pandas as pd
from psychopy import core
from psyflow import (BlockUnit, StimBank, StimUnit, SubInfo, TaskSettings, context_from_config,
                     initialize_exp, initialize_triggers, load_config, parse_task_run_options, runtime_context)
from src import generate_trial_plans, run_trial, summarize_trials

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {"human": "config/config.yaml", "qa": "config/config_qa.yaml", "sim": "config/config_scripted_sim.yaml"}


def _block(name: str, idx: int, plans: list[Any], settings: TaskSettings, win: Any, kb: Any,
           bank: StimBank, triggers: Any, sink: list[dict[str, Any]]) -> None:
    (BlockUnit(block_id=name, block_idx=idx, settings=settings, window=win, keyboard=kb)
     .add_condition(plans).on_start(lambda _: triggers.send(settings.triggers.get("block_start")))
     .on_end(lambda _: triggers.send(settings.triggers.get("block_end")))
     .run_trial(partial(run_trial, stim_bank=bank, trigger_runtime=triggers, block_id=name, block_idx=idx)).to_dict(sink))


def run(options) -> None:
    root = Path(__file__).resolve().parent; cfg = load_config(str(options.config_path))
    output, scope, ctx = None, nullcontext(), None
    if options.mode in ("qa", "sim"):
        ctx = context_from_config(task_dir=root, config=cfg, mode=options.mode); output, scope = ctx.output_dir, runtime_context(ctx)
    with scope:
        if options.mode == "qa": subject = {"subject_id": "qa"}
        elif options.mode == "sim": subject = {"subject_id": str(ctx.session.participant_id or "sim")}
        else: subject = SubInfo(cfg["subform_config"]).collect()
        settings = TaskSettings.from_dict(cfg["task_config"]); settings.add_subinfo(subject)
        if output is not None: settings.save_path = str(output)
        if options.mode == "qa" and output is not None:
            output.mkdir(parents=True, exist_ok=True); settings.res_file = str(output / "qa_trace.csv")
            settings.log_file = str(output / "qa_psychopy.log"); settings.json_file = str(output / "qa_settings.json")
        settings.triggers = cfg["trigger_config"]
        triggers = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)
        win, kb = initialize_exp(settings); bank = StimBank(win, cfg["stim_config"]).preload_all(); settings.save_to_json()
        triggers.send(settings.triggers.get("experiment_start"))
        StimUnit("instruction", win, kb, runtime=triggers).add_stim(bank.get("instruction")).wait_and_continue()
        seed = int(settings.plan_seed); practice_rows: list[dict[str, Any]] = []
        practice = generate_trial_plans(repetitions_per_cell=int(settings.practice_repetitions_per_cell), seed=seed, is_practice=True)
        _block("practice", -1, practice, settings, win, kb, bank, triggers, practice_rows)
        p = summarize_trials([{**row, "is_practice": False} for row in practice_rows])
        StimUnit("practice_summary", win, kb, runtime=triggers).add_stim(bank.get_and_format("practice_summary", accuracy=f"{p['accuracy']:.1%}")).wait_and_continue()
        rows: list[dict[str, Any]] = []
        scored = generate_trial_plans(repetitions_per_cell=int(settings.scored_repetitions_per_cell), seed=seed, is_practice=False)
        _block("scored", 0, scored, settings, win, kb, bank, triggers, rows)
        summary = summarize_trials(rows)
        StimUnit("good_bye", win, kb, runtime=triggers).add_stim(bank.get_and_format(
            "good_bye", accuracy=f"{summary['accuracy']:.1%}", max_k=f"{summary['max_k']:.2f}",
            k2=f"{summary['set_2_k']:.2f}", k4=f"{summary['set_4_k']:.2f}",
            k6=f"{summary['set_6_k']:.2f}", k8=f"{summary['set_8_k']:.2f}")).wait_and_continue(terminate=True)
        triggers.send(settings.triggers.get("experiment_end")); pd.DataFrame(rows).to_csv(settings.res_file, index=False); triggers.close(); core.quit()


def main() -> None:
    run(parse_task_run_options(task_root=Path(__file__).resolve().parent, description="Run visual change detection task",
                               default_config_by_mode=DEFAULT_CONFIG_BY_MODE, modes=MODES))
if __name__ == "__main__": main()

