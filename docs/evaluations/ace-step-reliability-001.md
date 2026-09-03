# ACE-Step Reliability Benchmark 001

## Decision question

Can the selected ACE-Step 1.5 XL Turbo + Official VAE configuration generate five consecutive
two-minute instrumentals reliably and fast enough for a personal local-production workflow?

This benchmark measures technical repeatability first. Musical acceptance remains a listening
decision and is recorded separately below.

## Fixed setup

| Parameter | Value |
| --- | --- |
| ACE-Step revision | `ca1e85fe9430179831e6bc6be790c332190a3866` |
| DiT / VAE | `acestep-v15-xl-turbo` / Official VAE |
| Planner | `acestep-5Hz-lm-1.7B`, MLX backend |
| Machine | Apple Silicon M4 Pro, 64 GB unified memory |
| Duration | 120 seconds |
| Tempo / key / meter | 68 BPM / C Major / 4/4 |
| Thinking / CoT caption | enabled / enabled |
| Inference | 8 steps, shift 3.0, ODE, batch 1 |
| Output | stereo WAV, 48 kHz, normalized to -1 dBFS peak |

The caption and section-tag timeline are identical to structure benchmark B. Only the seed changes.
Requests run sequentially to match personal use and avoid hiding memory pressure through parallel
execution.

## Generation results

| Track | Seed | End-to-end time | Status |
| --- | ---: | ---: | --- |
| 01 | `20260904` | 59.79s | succeeded |
| 02 | `20260905` | 83.29s | succeeded |
| 03 | `20260906` | 64.91s | succeeded |
| 04 | `20260907` | 70.03s | succeeded |
| 05 | `20260908` | 73.38s | succeeded |

- Successful requests: 5/5.
- Total generation time: **351.40 seconds (5 minutes 51.40 seconds)**.
- Mean / median: 70.28s / 70.03s per two-minute track.
- Range: 59.79–83.29s.
- Output produced: 600 seconds of audio in 351.40 seconds, approximately **1.71× real time**.
- Track 02's diffusion phase briefly slowed, but later runs recovered; there was no monotonic
  slowdown or cumulative failure.

While the service was active, sampled macOS memory headroom remained between 59% and 79%. It
returned to 95% after shutdown. No out-of-memory error, crash, or throttled-memory event occurred.
These are point-in-time system measurements, not a continuous profiler trace.

## File validation

| Track | RMS | Last 3s RMS | Outro drop | HF right minus left | SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| 01 | -17.03 dBFS | -63.15 dBFS | -46.11 dB | +5.39 dB | `3fb9ba714993ca31de3f326cf1dbc804a185a3bbdfc1395b8cfdffe56abd4b93` |
| 02 | -15.46 dBFS | -63.51 dBFS | -48.06 dB | +6.64 dB | `080fc5958068da46d828bbcf3c7a4ae7d67aa873a7dba328bf33371af88c6f21` |
| 03 | -15.54 dBFS | -64.52 dBFS | -48.98 dB | -0.51 dB | `97738c4d8df72add3df006fbbbcd21cd06d1aef795257e1702355d0e7975bc84` |
| 04 | -15.07 dBFS | -63.53 dBFS | -48.46 dB | +4.41 dB | `c0eca399bdad97eff75d1b912f5a8a610f78a50eaa3884bf517c8d8bc8ef6f14` |
| 05 | -15.48 dBFS | -63.66 dBFS | -48.18 dB | +3.60 dB | `f1e0eb4c29b6fc5924c5ca61485787d04139befd705e298fb5256b1e42a30670` |

All files are distinct, 120.0 seconds long, stereo, and 48 kHz. Every render has a 46–49 dB
level reduction in its final three seconds, so none ends with a hard cut.

The `HF right minus left` column compares aggregate energy above 6 kHz. Four of five renders lean
right in this band, matching the known harsh/right-biased hi-hat artifact identified during
listening. This limitation is accepted for the current generation of music models and is tracked
rather than treated as an ACE-Step rejection criterion.

## Local files

```text
outputs/ace-step/reliability-benchmark-001/01-seed-20260904.wav
outputs/ace-step/reliability-benchmark-001/02-seed-20260905.wav
outputs/ace-step/reliability-benchmark-001/03-seed-20260906.wav
outputs/ace-step/reliability-benchmark-001/04-seed-20260907.wav
outputs/ace-step/reliability-benchmark-001/05-seed-20260908.wav
```

The WAV files are local evaluation artifacts and remain excluded from Git.

## Listening result — 2026-09-03

| Track | Result |
| --- | --- |
| 01 | Good overall sound and fewer drum errors, but strongly repetitive; may be a lucky render |
| 02 | More musical variation, but audible drum-sound errors remain |
| 03 | Poor ensemble coherence: the players drift in and out of time, like a band rehearsing before a show |
| 04 | Neither good nor bad; a mediocre result |
| 05 | Similar ensemble-coherence failure to 03, but worse |

Interpretation:

- Technical reliability is 5/5, but musical reliability is at most 2/5. The run therefore fails
  the predeclared three-of-five acceptance gate.
- Track 01 shows that good sound is possible, but its repetition and the other four outcomes mean
  it cannot yet be treated as a repeatable baseline.
- Track 02 suggests that variation and clean rendering are partly independent variables.
- Tracks 03 and 05 expose a separate failure mode from drum timbre: timing and ensemble coherence.
  This points toward the planner/audio-code path rather than the VAE alone.
- Track 04 shows the middle of the distribution is merely acceptable, not compelling.

Outcome: do not begin broad UI integration yet. Re-test the known failing seeds with the larger 4B
planner while holding XL Turbo and Official VAE fixed. If the larger planner does not improve
ensemble coherence or repetition, move to reference-audio/Cover control rather than generating
more random text-to-music samples.

## Decision rule

- If at least three of five tracks are usable, accept ACE-Step as the local foundation and begin
  product-workflow integration.
- If the technical pass rate stays high but the musical pass rate is low, keep the engine and test
  reference-audio/Cover control before building broader UI.
- Treat the known high-frequency drum artifact as accepted technical debt unless a later model or
  post-processing step improves it without damaging the rest of the mix.
