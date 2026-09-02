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
- ACE-Step 1.5 is the next engine candidate because it officially supports Apple Silicon,
  instrumental structure, natural-language captions, and explicit outros.

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
