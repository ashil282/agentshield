from agentshield.models import Finding, Severity
from agentshield.scoring import calculate_risk


def test_risk_score_is_bounded():
    findings = [Finding(rule_id=str(i), title="x", severity=Severity.critical,
                        description="x", evidence="x") for i in range(5)]
    assert calculate_risk(findings) == 100

def test_empty_findings_have_zero_risk():
    assert calculate_risk([]) == 0
