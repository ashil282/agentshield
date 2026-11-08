from dataclasses import dataclass
from .engine import SecurityEngine
from .models import RunResult, Scenario

@dataclass(frozen=True)
class ReplayComparison:
    original_run_id: str
    replay_run_id: str
    identical: bool
    original_observed: str
    replay_observed: str
    original_score: int
    replay_score: int
    original_findings: tuple[str, ...]
    replay_findings: tuple[str, ...]

def _fingerprint(result: RunResult):
    return (
        result.observed,
        result.score,
        tuple(sorted(f.rule_id for f in result.findings)),
        tuple(sorted((a.tool, repr(a.arguments)) for a in result.actions)),
    )

class ReplayEngine:
    """Re-executes a scenario in the deterministic simulator and compares semantics."""
    def __init__(self, engine: SecurityEngine | None = None):
        self.engine = engine or SecurityEngine()

    def replay(self, scenario: Scenario, original: RunResult) -> tuple[RunResult, ReplayComparison]:
        if scenario.id != original.scenario_id:
            raise ValueError("Scenario ID does not match the original run")
        replayed = self.engine.run(scenario)
        same = _fingerprint(original) == _fingerprint(replayed)
        comparison = ReplayComparison(
            original_run_id=original.run_id,
            replay_run_id=replayed.run_id,
            identical=same,
            original_observed=original.observed,
            replay_observed=replayed.observed,
            original_score=original.score,
            replay_score=replayed.score,
            original_findings=tuple(sorted(f.rule_id for f in original.findings)),
            replay_findings=tuple(sorted(f.rule_id for f in replayed.findings)),
        )
        return replayed, comparison
