# AI Music Open

AI Music Open is a self-hosted workspace for evaluating and operating open AI music models. Its
goal is technological independence: produce complete music locally without depending on a single
commercial provider or model vendor.

## Principles

- Model-agnostic: HeartMuLa, ACE-Step, and future engines are replaceable adapters.
- Local-first: generation should run on hardware controlled by the user whenever practical.
- Output-driven: musical quality, structure, duration, stability, and speed decide which engine wins.
- Open and inspectable: application code, model integration, and evaluation results remain under
  the user's control.

## Current status

- HeartMuLa's official CUDA runtime has been reviewed.
- A community MLX port was validated on Apple Silicon for 120- and 180-second generation.
- The Mac M4 Pro with 64 GB unified memory handled the workload without memory pressure, but the
  instrumental output did not meet the required musical-quality threshold.
- ACE-Step 1.5 XL Turbo completed a 120-second instrumental locally in about 68 seconds with
  promising composition behavior and a natural outro. Its tendency toward loop-based structure is
  being evaluated with controlled temporal prompting. The first A/B/C test confirmed that temporal
  prompts can improve deliberate structure, but prompting alone did not improve audio fidelity.
  A subsequent VAE test selected the Official VAE over ScragVAE for sound quality. Harsh or
  right-biased high-frequency drum artifacts remain a known, accepted limitation rather than a
  rejection criterion. The Official VAE configuration then completed five consecutive two-minute
  renders without failure in 5 minutes 51.40 seconds total. Listening found only one or two
  candidate-usable renders: repetition and ensemble timing remain too inconsistent for product
  integration. The next controlled test targets the planner using the known failing seeds.

The first controlled ACE-Step structure experiment is documented in
[`docs/evaluations/ace-step-structure-001.md`](docs/evaluations/ace-step-structure-001.md).
The current official-VAE versus ScragVAE fidelity experiment is documented in
[`docs/evaluations/ace-step-fidelity-001.md`](docs/evaluations/ace-step-fidelity-001.md).
The five-track local reliability experiment is documented in
[`docs/evaluations/ace-step-reliability-001.md`](docs/evaluations/ace-step-reliability-001.md).

No engine is considered the permanent foundation of this project until it passes listening and
performance acceptance tests on the target machine.

## Repository layout

```text
apps/web/               Experimental Next.js interface
src/ai_music_open/      FastAPI API and asynchronous generation worker
tests/                  Backend contract tests
scripts/                Engine-specific setup helpers
```

## Experimental application shell

The repository currently contains an early FastAPI, Redis/RQ, and Next.js shell. It is not the
product architecture decision. The generation boundary is intentionally isolated so an engine can
be updated, forked, or replaced without rewriting the API.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
make install
make test
```

The existing HeartMuLa dependency and checkpoint helper are retained only as an experimental
adapter. ACE-Step evaluation will be added separately after it passes a local proof of concept.
