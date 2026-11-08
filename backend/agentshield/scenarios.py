import json
from pathlib import Path

from .models import Scenario

CATALOG=Path(__file__).resolve().parents[2]/"scenarios"/"catalog.json"
def load_scenarios(path=None):
    return [Scenario.model_validate(x) for x in json.loads(Path(path or CATALOG).read_text())]
def get_scenario(scenario_id,path=None):
    return next((s for s in load_scenarios(path) if s.id==scenario_id),None)
