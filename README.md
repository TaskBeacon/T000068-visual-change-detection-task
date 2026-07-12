# Visual Change Detection Task

| Field | Value |
|---|---|
| Name | Visual Change Detection Task |
| Version | 0.1.0 |
| Date Updated | 2026-07-12 |
| PsyFlow Version | current local runtime |
| PsychoPy Version | current local runtime |
| Modality | Behavioral |
| Language | English |
| TaskBeacon ID | T000068 |
| Variant | Color change detection |

## 1. Task Overview

This implementation measures visual working-memory capacity with the classic brief color-array change-detection paradigm. Participants remember two, four, six, or eight colored squares across a short retention interval and report whether the test array is identical or contains one color change. Same and change trials are balanced at every set size.

The task records accuracy and response time and derives hit rate, false-alarm rate, and Cowan K for each set size. The canonical human protocol contains eight practice trials and 160 scored trials. Trial plans are deterministic for auditability while retaining randomized positions, colors, changed item, and trial order.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

`Instruction -> Practice (8 trials) -> Practice summary -> Scored block (160 trials) -> Capacity summary`

### Trial-Level Flow

`Fixation (500 ms) -> Memory array (100 ms) -> Retention (900 ms) -> Test array (F/J, <=2000 ms)`

On a same trial, the sample and test arrays are identical. On a change trial, exactly one sampled square changes to a color that was absent from the memory array; all positions remain fixed.

### Controller Logic

There is no adaptive controller. A seeded planner balances the 4 x 2 factorial design and realizes unique sample colors at a random subset of eight fixed locations. The changed index and replacement color are selected before trial execution and logged with the plan.

### Other Logic

F reports SAME and J reports CHANGE. Responses end the test display. Timeouts are logged without feedback. Capacity at set size N is `K = N * (hit rate - false-alarm rate)`.

## 3. Configuration Summary

### a. Subject Info

| Field | Type | Constraint |
|---|---|---|
| Participant ID | Integer | Three digits, 101-999 |

### b. Window Settings

| Setting | Value |
|---|---|
| Resolution | 1280 x 800 |
| Units | Degrees of visual angle |
| Background | Near black (`#101216`) |
| Viewing distance | 50 cm |

### c. Stimuli

| Stimulus | Definition |
|---|---|
| Fixation | Central white plus |
| Memory array | 2, 4, 6, or 8 unique-color 1.25-degree squares |
| Retention | Fixation only |
| Test array | Same array or exactly one color replacement |

### d. Timing

| Phase | Human Duration |
|---|---:|
| Fixation | 500 ms |
| Memory array | 100 ms |
| Retention | 900 ms |
| Test/response | Up to 2000 ms |

### Triggers

| Event | Codes |
|---|---|
| Experiment/block boundaries | 1, 10, 90, 99 |
| Fixation/retention | 20, 30 |
| Memory set size 2/4/6/8 | 22, 24, 26, 28 |
| Test same/change | 40, 41 |
| Response same/change/timeout | 50, 51, 52 |

### Adaptive Controller

Not applicable. The condition plan is balanced and fixed before the block.

## 4. Methods (for academic publication)

Participants completed a visual change-detection task adapted from the color-array procedures of Luck and Vogel (1997) and Vogel, Woodman, and Luck (2001). Each trial began with a 500-ms fixation, followed by a 100-ms memory array containing 2, 4, 6, or 8 uniquely colored squares. After a 900-ms retention interval, a test array appeared at the same locations. On half of trials the test was identical; on the remaining trials exactly one square changed to a color absent from the sample array. Participants pressed F for same and J for change within 2000 ms. The scored block contained 20 trials in each set-size by test-status cell. For each set size N, capacity was estimated as `K = N * (H - FA)`, where H is the change-trial hit rate and FA is the same-trial false-alarm rate.

## Running the Task

```powershell
python main.py human --config config/config.yaml
python main.py qa --config config/config_qa.yaml
python main.py sim --config config/config_scripted_sim.yaml
python main.py sim --config config/config_sampler_sim.yaml
```

## References

- Luck, S. J., & Vogel, E. K. (1997). The capacity of visual working memory for features and conjunctions. *Nature*. https://doi.org/10.1038/36846
- Vogel, E. K., Woodman, G. F., & Luck, S. J. (2001). Storage of features, conjunctions, and objects in visual working memory. *Journal of Experimental Psychology: Human Perception and Performance*. https://doi.org/10.1037/0096-1523.27.1.92
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X01003922
