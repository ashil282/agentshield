from fastapi import FastAPI, HTTPException, Query
import os
from .engine import SecurityEngine
from .scenarios import load_scenarios,get_scenario
from .storage import RunStore
app=FastAPI(title="AgentShield API",version="1.0.0",description="Local-first agent security simulation API")
engine=SecurityEngine()
store=RunStore(os.getenv("AGENTSHIELD_DB","agentshield.db"))
@app.get("/health")
def health(): return {"status":"ok","mode":"local-simulation"}
@app.get("/api/v1/scenarios")
def scenarios(): return [s.model_dump(mode="json") for s in load_scenarios()]
@app.post("/api/v1/runs")
def create_run(payload:dict):
    scenario=get_scenario(payload.get("scenario_id",""))
    if scenario is None: raise HTTPException(404,"Unknown scenario_id")
    result=engine.run(scenario); store.save(result)
    return result.model_dump(mode="json")
@app.get("/api/v1/runs")
def list_runs(limit:int=Query(50,ge=1,le=500)): return store.list(limit)
@app.get("/api/v1/runs/{run_id}")
def get_run(run_id:str):
    result=store.get(run_id)
    if result is None: raise HTTPException(404,"Run not found")
    return result
