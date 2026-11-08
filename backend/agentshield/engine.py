from datetime import datetime, timezone
from uuid import uuid4

from .detection import inspect_action, inspect_text
from .models import RunResult
from .policies import PolicyEngine
from .scoring import calculate_risk
from .simulator import SimulatedAgent


class SecurityEngine:
    def __init__(self, policy=None, agent=None):
        self.policy=policy or PolicyEngine()
        self.agent=agent or SimulatedAgent()
    def run(self, scenario):
        started=datetime.now(timezone.utc)
        findings=inspect_text(scenario.input_text)
        actions=self.agent.propose(scenario)
        observed="blocked" if findings else "no_heuristic_match"
        for action in actions:
            decision,_=self.policy.evaluate(action)
            if decision.value!="allow":
                observed="blocked" if decision.value=="deny" else "approval_required"
            findings.extend(inspect_action(action))
        unique={(f.rule_id,f.action_id):f for f in findings}
        findings=list(unique.values())
        score=calculate_risk(findings)
        passed=(scenario.expected=="block" and observed=="blocked") or (scenario.expected=="allow" and observed=="no_heuristic_match") or (scenario.expected=="approval_required" and observed=="approval_required")
        return RunResult(run_id=str(uuid4()),scenario_id=scenario.id,status="completed",
            expected=scenario.expected,observed=observed,passed=passed,score=score,findings=findings,
            actions=actions,started_at=started,finished_at=datetime.now(timezone.utc))
