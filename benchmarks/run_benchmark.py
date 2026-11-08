#!/usr/bin/env python3
"""Small deterministic benchmark over the bundled synthetic catalog."""
import json
from collections import defaultdict
from pathlib import Path
from agentshield.engine import SecurityEngine
from agentshield.scenarios import load_scenarios

def main():
    results = [SecurityEngine().run(s) for s in load_scenarios()]
    groups = defaultdict(lambda: {"total": 0, "passed": 0, "mean_risk": 0})
    for r in results:
        g = groups[r.scenario_id.split("-")[0]]
        g["total"] += 1
        g["passed"] += int(r.passed)
        g["mean_risk"] += r.score
    for g in groups.values():
        g["mean_risk"] = round(g["mean_risk"] / g["total"], 2)
        g["pass_rate"] = round(100 * g["passed"] / g["total"], 1)
    summary = {"scenarios": len(results), "passed": sum(r.passed for r in results),
               "failed": sum(not r.passed for r in results), "groups": dict(groups)}
    Path("benchmark-results.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0 if summary["failed"] == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
