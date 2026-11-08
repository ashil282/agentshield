from agentshield.engine import SecurityEngine
from agentshield.replay import ReplayEngine
from agentshield.scenarios import load_scenarios


def test_replay_is_semantically_deterministic():
    scenario = load_scenarios()[0]
    engine = SecurityEngine()
    original = engine.run(scenario)
    replayed, comparison = ReplayEngine(engine).replay(scenario, original)
    assert replayed.run_id != original.run_id
    assert comparison.identical

def test_replay_rejects_wrong_scenario():
    scenarios = load_scenarios()
    engine = SecurityEngine()
    original = engine.run(scenarios[0])
    try:
        ReplayEngine(engine).replay(scenarios[1], original)
    except ValueError as exc:
        assert "does not match" in str(exc)
    else:
        raise AssertionError("Expected scenario mismatch to fail")
