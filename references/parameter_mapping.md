# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| P01 | timing.memory_duration | 0.100 s | VOGEL2001 | Method describes a 100-ms sample array | direct | Preserved in human config |
| P02 | timing.retention_duration | 0.900 s | VOGEL2001 | Method describes a 900-ms retention interval | direct | Fixation remains visible |
| P03 | task.conditions | set sizes 2, 4, 6, 8 x same/change | LUCK1997; VOGEL2001 | Accuracy is measured over increasing array sizes with identical and changed tests | adapted | Extends sampling around the canonical 3-4 item limit |
| P04 | task.scored_repetitions_per_cell | 20 | inferred | No single required trial count across source experiments | inferred | Gives 160 scored trials and balanced cell estimates |
| P05 | task.practice_repetitions_per_cell | 1 | inferred | Practice count is not diagnostic to the paradigm | inferred | One exposure to each factorial cell |
| P06 | timing.fixation_duration | 0.500 s | inferred | Stable pre-sample baseline required | inferred | Fixed rather than jittered |
| P07 | timing.response_window | 2.000 s | inferred | Unspeeded same/change judgment in source family | inferred | Timeout logged; no feedback |
| P08 | task.square_size_deg | 1.25 deg | VOGEL2001 | Small colored squares distributed around fixation | adapted | Sized for an eight-location 1280x800 display |
| P09 | summary K | N x (hit rate - false-alarm rate) | COWAN2001 | Capacity derived from set size and corrected detection performance | direct | Reported separately at each set size |

