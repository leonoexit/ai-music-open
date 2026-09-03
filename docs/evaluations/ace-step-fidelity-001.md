# ACE-Step Fidelity Benchmark 001

## Decision question

Does ScragVAE materially improve the audible fidelity of the current ACE-Step 1.5 XL Turbo setup
on Apple Silicon, compared with ACE-Step's official VAE?

This is the first fidelity experiment after the structure benchmark. It keeps variant B as the
musical reference and changes the VAE checkpoint only. ScragVAE is a compatible MIT-licensed
decoder that specifically targets high-frequency loss, transient detail, and perceived air in the
official VAE.

Sources:

- [ScragVAE model card](https://huggingface.co/scragnog/Ace-Step-1.5-ScragVAE)
- [ACE-Step Apple Silicon XL base/SFT corruption report](https://github.com/ace-step/ACE-Step-1.5/issues/1259)

## Why this variable was tested first

The previous A/B/C benchmark found useful differences in composition and structure, but no
meaningful difference in sound quality. A VAE change is closer to the waveform rendering path than
further prompt engineering or a larger language planner.

XL SFT was not downloaded for this round. Open ACE-Step reports currently describe reproducible
garbled output from non-distilled XL base/SFT models on Apple Silicon while Turbo works normally.
That makes a roughly 20 GB SFT download a poor first diagnostic until the Mac-specific behavior is
resolved or independently reproduced.

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
| Output | stereo WAV, 48 kHz, normalized to -1 dBFS peak |

Both variants use the caption and section-tag timeline from structure benchmark B. The only
declared model change is `ACESTEP_VAE_CHECKPOINT`: official VAE versus `scragvae`.

## Files

| Variant | Local output | SHA-256 |
| --- | --- | --- |
| Official VAE | `outputs/ace-step/fidelity-benchmark-001/official-vae-B-seed-20260903.wav` | `9cf1cf6567f095334ea45b77a47841d14f0b69d840c77a8a9ade9da3689009bd` |
| ScragVAE | `outputs/ace-step/fidelity-benchmark-001/scragvae-B-seed-20260903.wav` | `8ad1854bf1ba6ecd5a32fac4acb8541ee258037bc906acab3314d83072720247` |

The WAV files are local evaluation artifacts and remain excluded from Git.

## Technical results

| Metric | Official VAE | ScragVAE |
| --- | ---: | ---: |
| Duration | 120.0s | 120.0s |
| Peak | -1.00 dBFS | -1.00 dBFS |
| RMS | -15.46 dBFS | -14.67 dBFS |
| Last 3s RMS | -63.90 dBFS | -40.07 dBFS |
| Energy above 8 kHz | 0.0639% | 0.0330% |
| Energy above 12 kHz | 0.0056% | 0.0081% |
| Spectral centroid | 256.1 Hz | 186.5 Hz |
| 95% spectral rolloff | 697.3 Hz | 527.3 Hz |

ScragVAE generation took approximately 60 seconds end-to-end. Its measured diffusion phase was
22.94 seconds and VAE decode was 14.57 seconds.

The objective measurements are mixed: ScragVAE adds energy above 12 kHz in this sample, but has
less energy above 8 kHz and a lower overall spectral centroid. It is also approximately 0.8 dB
louder by RMS and leaves more energy in the final three seconds. These values do not establish an
audible quality win; they only prevent us from assuming that the alternate decoder is automatically
brighter or cleaner on this track.

This is an end-to-end fixed-seed comparison, not an identical-latent decoder-only laboratory test.
The VAE can participate in model conditioning, so small musical differences may exist between the
renders even with the same prompt and seed. A direct latent replay should be added later if this
first listening test is close enough to justify deeper decoder work.

## Listening scorecard

Use headphones if practical. Ignore small loudness differences and focus on artifact character.

| Dimension | Official VAE | ScragVAE |
| --- | ---: | ---: |
| Piano transient and note definition |  |  |
| Brush texture and upper-frequency air |  |  |
| Upright-bass separation |  |  |
| Low distortion / metallic artifacts |  |  |
| Natural outro |  |  |
| Overall fidelity |  |  |

## Decision rule

- Adopt ScragVAE for the next benchmark only if it is audibly cleaner or more natural, not merely
  different or louder.
- If neither render clears the sound-quality threshold, do not spend more time polishing the UI.
  Move to decoder-only replay and reference-audio/Cover tests before considering a different engine.
- If ScragVAE is worse, restore the official VAE and treat the decoder as a ruled-out first-order
  fix for this configuration.

## Listening result — 2026-09-03

| Question | Result |
| --- | --- |
| Better overall sound | Official VAE |
| Less obvious repetition | ScragVAE |
| Decoder selected for continued work | Official VAE |

Interpretation:

- ScragVAE changes the result but does not improve the target dimension. Its lower repetition is
  interesting, but it does not compensate for the loss in overall sound quality.
- Because this was an end-to-end render rather than an identical-latent replay, the repetition
  difference must not be attributed to decoder fidelity alone.
- Restore the official VAE as the project default. ScragVAE is ruled out as the first-order sound
  quality fix for this configuration.
- Harsh hi-hats and a tendency for the high-frequency drum image to drift right are accepted as a
  current-generation model limitation. The same class of artifact is also heard in commercial
  systems; it should be tracked, but it is not an ACE-Step rejection criterion for this project.

Outcome: the Official VAE configuration advances to the next stage. Further work should prioritize
repeatability and user control over chasing this known drum artifact.
