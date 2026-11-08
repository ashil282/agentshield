from .models import Finding, Severity

WEIGHTS = {
    Severity.info: 1,
    Severity.low: 5,
    Severity.medium: 15,
    Severity.high: 30,
    Severity.critical: 50,
}

def calculate_risk(findings: list[Finding]) -> int:
    """Return a bounded heuristic score, not a probability or exploitability estimate."""
    return min(100, sum(WEIGHTS[f.severity] for f in findings))
