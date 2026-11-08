# Architecture

## Components
- `models.py`: Pydantic scenario/action/finding/run contracts.
- `detection.py`: local heuristic inspection of text and action metadata.
- `simulator.py`: deterministic mapping from scenario language to inert actions.
- `policies.py`: allowlist, denylist and approval decision engine.
- `engine.py`: orchestration, outcome comparison and bounded risk aggregation.
- `storage.py`: SQLite run persistence.
- `reporting.py`: escaped HTML and JSON reports.
- `api.py`: FastAPI interface.
- `frontend/`: React dashboard.

## Lifecycle
Load and validate a scenario; inspect input; propose inert simulated actions; evaluate policy; inspect action metadata; deduplicate findings; calculate risk; compare expected/observed result; persist and report.

## Trust boundaries
Scenario text is untrusted. It is never evaluated as Python, shell, SQL or JavaScript. Actions are records only. HTML report values are escaped; React renders strings as text.

## v1 constraints
No live agent adapters, semantic model evaluation, tenant isolation, signed policy bundles or distributed workers. See roadmap for future work.

## Replay and benchmarking
`ReplayEngine` reruns a scenario and compares stable semantic fingerprints: observed result, score, finding IDs and proposed tool actions. `benchmarks/run_benchmark.py` aggregates deterministic catalog outcomes. These are regression checks, not representative external benchmarks.
