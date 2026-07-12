# Task Logic Audit

## 1. Paradigm Intent

The task estimates visual working-memory capacity by manipulating array set size (2, 4, 6, or 8 colored squares) and test status (same or one color changed). The dependent measures are same/change accuracy, hit rate, false-alarm rate, response time, and Cowan K.

## 2. Block/Trial Workflow

An eight-trial practice block contains one trial per factorial cell. A 160-trial scored block contains 20 trials per cell. Trial plans are generated deterministically from an independent plan seed and shuffled within each block. Each trial follows `fixation (500 ms) -> memory_array (100 ms) -> retention (900 ms) -> test_array (up to 2000 ms or response)`.

## 3. Condition Semantics

The memory array contains uniquely colored squares at a random subset of eight fixed, well-separated locations. A same test repeats every color and location. A change test preserves every location and changes exactly one color to a palette color absent from the memory array. No abstract condition token appears on screen.

## 4. Response and Scoring Rules

F means same and J means change. A response terminates the test array. Missing the 2-second deadline yields `timeout`; no correctness feedback is shown. Change trials yield hit or miss, while same trials yield correct rejection or false alarm. Accuracy is the proportion correct. For each set size N, `K = N * (hit rate - false-alarm rate)`. Maximum K summarizes the largest observed set-size estimate. There is no adaptive controller, reward, or cross-trial state update.

## 5. Stimulus Layout Plan

Eight candidate positions form three rows around fixation with at least 4.5 degrees horizontal and 2.8 degrees vertical center spacing. Squares are 1.25 degrees, preventing overlap. Both arrays use identical sampled positions and scale.

## 6. Trigger Plan

Experiment and block boundaries have dedicated triggers. Fixation and retention have phase triggers; memory-array triggers identify set size; test-array triggers identify same/change; responses distinguish F, J, and timeout.

## 7. Architecture Decisions (Auditability)

The implementation uses primitives, deterministic plans, PsyFlow trial identity, StimUnit timing and response capture, and phase-level context logging. Core factors are preplanned rather than selected inside `run_trial` because item-level colors, positions, and the changed index must remain replayable while enforcing unique colors.

## 8. Inference Log

The 500-ms fixation, 2-second response deadline, eight practice trials, 160 scored trials, fixed eight-location layout, and F/J key mapping are implementation decisions because the selected literature does not require one universal value. These choices do not alter the defining 100-ms sample, 900-ms retention, same/change manipulation, or K estimator.
