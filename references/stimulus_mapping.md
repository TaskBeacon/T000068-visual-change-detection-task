# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| all | fixation | fixation | Central white plus on dark field | VOGEL2001 | Fixation maintained through trial | PsychoPy text primitive | none | Central anchor |
| set size 2/4/6/8 | memory_array | color_square | Two to eight uniquely colored squares at sampled fixed locations | LUCK1997; VOGEL2001 | Brief multicolor sample array | PsychoPy rect primitives | none | Colors and positions logged |
| all | retention | fixation | Blank dark field with central fixation | VOGEL2001 | 900-ms retention interval | PsychoPy text primitive | none | No memory items visible |
| same | test_array | color_square | Exact repetition of sample colors at the same locations | LUCK1997 | Same test-array trials | PsychoPy rect primitives | none | Correct response F |
| change | test_array | color_square | Same positions with exactly one square replaced by a previously unused color | LUCK1997 | One-item color change | PsychoPy rect primitives | none | Correct response J; changed index logged |
| `set_2_same` | full trial | fixation; color_square | Two colored squares followed by an identical two-square test | LUCK1997 | Set-size manipulation and same test | PsychoPy primitives | none | Explicit factorial cell |
| `set_2_change` | full trial | fixation; color_square | Two colored squares followed by one color replacement | LUCK1997 | Set-size manipulation and one-item change | PsychoPy primitives | none | Explicit factorial cell |
| `set_4_same` | full trial | fixation; color_square | Four colored squares followed by an identical four-square test | LUCK1997 | Set-size manipulation and same test | PsychoPy primitives | none | Explicit factorial cell |
| `set_4_change` | full trial | fixation; color_square | Four colored squares followed by one color replacement | LUCK1997 | Set-size manipulation and one-item change | PsychoPy primitives | none | Explicit factorial cell |
| `set_6_same` | full trial | fixation; color_square | Six colored squares followed by an identical six-square test | LUCK1997 | Set-size manipulation and same test | PsychoPy primitives | none | Explicit factorial cell |
| `set_6_change` | full trial | fixation; color_square | Six colored squares followed by one color replacement | LUCK1997 | Set-size manipulation and one-item change | PsychoPy primitives | none | Explicit factorial cell |
| `set_8_same` | full trial | fixation; color_square | Eight colored squares followed by an identical eight-square test | LUCK1997 | Set-size manipulation and same test | PsychoPy primitives | none | Explicit factorial cell |
| `set_8_change` | full trial | fixation; color_square | Eight colored squares followed by one color replacement | LUCK1997 | Set-size manipulation and one-item change | PsychoPy primitives | none | Explicit factorial cell |
