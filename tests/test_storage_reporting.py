from agentshield.engine import SecurityEngine
from agentshield.scenarios import load_scenarios
from agentshield.storage import RunStore
from agentshield.reporting import to_html,to_json
def test_sqlite_roundtrip(tmp_path):
    r=SecurityEngine().run(load_scenarios()[0]); db=RunStore(tmp_path/"runs.db"); db.save(r)
    assert db.get(r.run_id)["scenario_id"]==r.scenario_id and len(db.list())==1
def test_report_serialization_and_escape():
    r=SecurityEngine().run(load_scenarios()[0])
    assert "AgentShield security report" in to_html(r)
    assert '"scenario_id"' in to_json(r)
