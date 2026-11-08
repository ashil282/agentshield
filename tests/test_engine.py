from agentshield.engine import SecurityEngine
from agentshield.scenarios import load_scenarios
def test_catalog_size(): assert len(load_scenarios()) >= 10
def test_every_catalog_case_completes():
    results=[SecurityEngine().run(s) for s in load_scenarios()]
    assert all(r.status=="completed" and 0<=r.score<=100 for r in results)
def test_direct_injection_expected_result():
    s=next(x for x in load_scenarios() if x.id=="direct-ignore")
    r=SecurityEngine().run(s)
    assert r.observed=="blocked" and r.passed
