import argparse
import json
from pathlib import Path

from .engine import SecurityEngine
from .reporting import write_report
from .scenarios import get_scenario, load_scenarios
from .storage import RunStore


def main(argv=None):
    p=argparse.ArgumentParser(prog="agentshield",description="Local AI agent security test harness")
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("list")
    r=sub.add_parser("run"); r.add_argument("scenario_id"); r.add_argument("--db",default="agentshield.db"); r.add_argument("--report")
    s=sub.add_parser("suite"); s.add_argument("--db",default="agentshield.db"); s.add_argument("--report-dir",default="reports")
    a=p.parse_args(argv)
    if a.cmd=="list":
        for x in load_scenarios(): print(f"{x.id:20} {x.severity.value:8} {x.title}")
        return 0
    engine=SecurityEngine(); store=RunStore(a.db)
    if a.cmd=="run":
        scenario=get_scenario(a.scenario_id)
        if scenario is None: p.error(f"unknown scenario: {a.scenario_id}")
        result=engine.run(scenario); store.save(result); print(result.model_dump_json(indent=2))
        if a.report: write_report(result,a.report)
        return 0 if result.passed else 2
    out=Path(a.report_dir); results=[]
    for scenario in load_scenarios():
        result=engine.run(scenario); store.save(result); results.append(result)
        write_report(result,out/f"{scenario.id}.json")
    summary={"total":len(results),"passed":sum(x.passed for x in results),
             "failed":sum(not x.passed for x in results)}
    summary["pass_rate"]=round(100*summary["passed"]/summary["total"],1)
    out.mkdir(parents=True,exist_ok=True); (out/"summary.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    return 0 if summary["failed"]==0 else 2
if __name__=="__main__": raise SystemExit(main())
