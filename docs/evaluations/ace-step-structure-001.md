# ACE-Step Structure Benchmark 001

## Decision question

Can ACE-Step reduce obvious musical looping in a two-minute instrumental by using its `lyrics`
field as a temporal arrangement plan, without losing the sound quality and natural outro of the
initial successful result?

ACE-Step's official tutorial describes `caption` as the overall musical description and `lyrics`
as the temporal description for structure evolution, instrumental performance, and start/end
behavior. This benchmark changes only the `lyrics` plan while keeping the generation setup fixed.

## Fixed setup

| Parameter | Value |
| --- | --- |
| ACE-Step revision | `ca1e85fe9430179831e6bc6be790c332190a3866` |
| DiT | `acestep-v15-xl-turbo` |
| Planner | `acestep-5Hz-lm-1.7B`, MLX backend |
| Machine | Apple Silicon M4 Pro, 64 GB unified memory |
| Seed | `20260903` |
| Duration | 120 seconds |
| Tempo / key / meter | 68 BPM / C Major / 4/4 |
| Thinking / CoT caption | enabled / enabled |
| Inference | 8 steps, shift 3.0, ODE, batch 1 |
| Output | stereo WAV, 48 kHz |

All variants use this caption:

> The arrangement features a Japanese slow jazz piano trio: delicate piano leads with gentle,
> expressive phrasing, spacious upright bass lines, and soft brushed drums. The tempo is
> unhurried, creating a relaxed, inviting café atmosphere. Subtle jazz voicings provide warmth
> throughout.

## Variants

### A — Caption only

Control case with no explicit timeline:

```text
[Instrumental]
```

Local output: `outputs/ace-step/structure-benchmark-001/A-caption-only-seed-20260903.wav`

### B — Section tags

The initial successful two-minute result:

```text
[Instrumental]
[Intro - delicate piano]
[Main Theme - expressive piano trio]
[Development - spacious jazz voicings]
[Interlude - upright bass]
[Main Theme - warm reprise]
[Outro - gentle resolved ending]
[Fade Out]
```

Local output: `outputs/ace-step/structure-benchmark-001/B-section-tags-seed-20260903.wav`

### C — Through-composed timeline

Explicit development, contrast, and resolution instructions:

```text
[Instrumental]
[Intro - solo piano introduces a sparse four-bar motif, rubato, no drums]
[Theme A - bass and brushes enter; piano develops the motif with new voicings, avoid exact repetition]
[Development - move the melody to a higher register; expand the harmony and increase rhythmic motion]
[Piano and Bass Dialogue - bass leads a contrasting idea; piano answers; drums remain restrained]
[Theme B - introduce a genuinely new melody and chord movement, not a loop of Theme A]
[Climax - full trio at the strongest dynamic; reharmonize the earlier motif instead of repeating it verbatim]
[Resolution - gradually reduce density; resolve harmonic tension; do not return to the full opening loop]
[Outro - solo piano cadence ending on a final sustained chord]
[Fade Out]
```

Local output: `outputs/ace-step/structure-benchmark-001/C-through-composed-seed-20260903.wav`

## Technical results

| Variant | End-to-end time | Duration | Full-track RMS | Last 3s RMS | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| A | ~66s | 120.0s | -16.67 dB | -64.51 dB | valid |
| B | ~68s | 120.0s | -16.85 dB | -64.50 dB | valid |
| C | ~78s | 120.0s | -16.18 dB | -64.29 dB | valid |

All three files are distinct, stereo, 48 kHz, and finish with a measurable fade rather than a hard
cut. Variant C spends additional time in the LM planner; its diffusion time remains approximately
the same as A and B.

| Variant | SHA-256 |
| --- | --- |
| A | `4760222d3b5baeb6daefccf6741887e2577e57b18aa202b319e7f6aecd3eb909` |
| B | `9cf1cf6567f095334ea45b77a47841d14f0b69d840c77a8a9ade9da3689009bd` |
| C | `2a1d97cb9c67901337cbe0ff279ba2b463eec2451d0468616931cc3010b41aa2` |

## Listening scorecard

Score each dimension from 1 (poor) to 5 (excellent). Do not judge the file names as a quality
ranking; A/B/C describe prompt complexity only.

| Dimension | A | B | C |
| --- | ---: | ---: | ---: |
| Sound quality |  |  |  |
| Feels like a complete piece |  |  |  |
| Structural development |  |  |  |
| Low unwanted repetition |  |  |  |
| Prompt/style adherence |  |  |  |
| Intro/outro quality |  |  |  |
| Overall preference |  |  |  |

Known listening note for B: the result is promising and has a real outro, but its middle structure
feels relatively loop-based.

## Decision rule

Prefer C only if it improves structural development or unwanted repetition without materially
reducing sound quality, style adherence, or outro quality relative to B. If C wins, repeat B and C
across at least three new seeds to check that the improvement is reliable rather than accidental.
If neither structured prompt improves on A, investigate the 4B planner, model variants, or a
reference-audio/Cover workflow before product integration.
