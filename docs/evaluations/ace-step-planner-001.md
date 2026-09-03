# ACE-Step Planner Benchmark 001

## Decision question

Does replacing the 1.7B planner with `acestep-5Hz-lm-4B` improve ensemble timing, musical
coherence, or repetition on two seeds that previously failed listening evaluation?

This is a controlled planner test. XL Turbo, Official VAE, prompt, duration, inference settings,
and seed remain fixed within each pair.

## Fixed setup

| Parameter | Value |
| --- | --- |
| ACE-Step revision | `ca1e85fe9430179831e6bc6be790c332190a3866` |
| DiT / VAE | `acestep-v15-xl-turbo` / Official VAE |
| Planner backend | MLX |
| Planner variants | `acestep-5Hz-lm-1.7B` and `acestep-5Hz-lm-4B` |
| Machine | Apple Silicon M4 Pro, 64 GB unified memory |
| Seeds | `20260906` and `20260908` |
| Duration | 120 seconds |
| Tempo / key / meter | 68 BPM / C Major / 4/4 |
| Thinking / CoT caption | enabled / enabled |
| Inference | 8 steps, shift 3.0, ODE, batch 1 |
| Output | stereo WAV, 48 kHz, normalized to -1 dBFS peak |

The 4B checkpoint is 7.8 GiB across two safetensor shards. It loaded successfully with the native
MLX planner backend in approximately 20 seconds.

## Performance results

| Seed | 1.7B time | 4B time | 4B overhead |
| --- | ---: | ---: | ---: |
| `20260906` | 64.91s | 100.68s | +35.77s |
| `20260908` | 73.38s | 106.28s | +32.90s |
| Mean | 69.15s | 103.48s | +34.34s |

The 4B planner is approximately 50% slower end-to-end for these samples, but still generates a
two-minute track faster than real time. The first 4B audio-code pass took 46.74 seconds, versus
approximately 19–21 seconds in earlier 1.7B runs.

Sampled memory headroom was 52% during 4B generation and returned to 95% after service shutdown.
There was no out-of-memory error or crash.

## File validation

| Seed / planner | RMS | Last 3s RMS | Outro drop | HF right minus left | SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| `20260906` / 1.7B | -15.54 dBFS | -64.52 dBFS | -48.98 dB | -0.51 dB | `97738c4d8df72add3df006fbbbcd21cd06d1aef795257e1702355d0e7975bc84` |
| `20260906` / 4B | -14.71 dBFS | -49.35 dBFS | -34.64 dB | +2.65 dB | `04b8b65408d6df2903337cd6449489e7c3c803342e134af3e2042a17da7a97cd` |
| `20260908` / 1.7B | -15.48 dBFS | -63.66 dBFS | -48.18 dB | +3.60 dB | `f1e0eb4c29b6fc5924c5ca61485787d04139befd705e298fb5256b1e42a30670` |
| `20260908` / 4B | -14.88 dBFS | -63.34 dBFS | -48.47 dB | +2.38 dB | `a2109eaa9e57e8f2a3c2bdfc49821bebc8dccf43787ea72a005a9d7ba33f7e6f` |

All four files are distinct, 120.0 seconds long, stereo, and 48 kHz. Both 4B renders have a
measurable outro reduction rather than a hard cut. The 4B renders are 0.6–0.8 dB louder by RMS;
listening should not treat this small loudness advantage as improved quality.

## Local files

```text
outputs/ace-step/planner-benchmark-001/03-lm-1.7B-seed-20260906.wav
outputs/ace-step/planner-benchmark-001/03-lm-4B-seed-20260906.wav
outputs/ace-step/planner-benchmark-001/05-lm-1.7B-seed-20260908.wav
outputs/ace-step/planner-benchmark-001/05-lm-4B-seed-20260908.wav
```

The WAV files are local evaluation artifacts and remain excluded from Git.

## Listening questions

For each seed, compare 1.7B with 4B:

1. Does 4B keep the trio in time more consistently?
2. Does 4B reduce obvious repetition?
3. Does 4B improve the overall musical result enough to justify approximately 50% more time?

## Listening result — 2026-09-03

| 4B render | Result |
| --- | --- |
| Seed `20260906` | Temporarily acceptable; the known failure improved to a usable middle ground |
| Seed `20260908` | Still poor |

Interpretation:

- The 4B planner can change or improve an individual failure, but it did not repair both known bad
  seeds.
- A one-of-two improvement is not reliable enough to justify making generation approximately 50%
  slower by default.
- The larger planner is retained as an optional experiment, not the production default.
- Keep the 1.7B planner for speed and move the next controlled experiment to reference-audio/Cover
  control, where musical timing and structure are constrained by source material rather than left
  entirely to text-to-music sampling.

Outcome: 4B fails the predeclared adoption rule.

## Decision rule

- Select 4B only if it materially improves timing/coherence in both known failure cases.
- A merely different arrangement, higher loudness, or one lucky improvement is insufficient.
- If 4B does not reliably fix these failures, retain 1.7B for speed and move the next experiment to
  reference-audio/Cover control.
