import json
import sqlite3


class RunStore:
    def __init__(self,path="agentshield.db"):
        self.path=str(path)
        with self.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, scenario_id TEXT NOT NULL, created_at TEXT NOT NULL, payload TEXT NOT NULL)")
    def connect(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
    def save(self,result):
        with self.connect() as c:
            c.execute("INSERT OR REPLACE INTO runs VALUES(?,?,?,?)",
                (result.run_id,result.scenario_id,result.finished_at.isoformat(),result.model_dump_json()))
    def list(self,limit=100):
        with self.connect() as c:
            rows=c.execute("SELECT payload FROM runs ORDER BY created_at DESC LIMIT ?",(max(1,min(limit,500)),)).fetchall()
        return [json.loads(r["payload"]) for r in rows]
    def get(self,run_id):
        with self.connect() as c:
            r=c.execute("SELECT payload FROM runs WHERE run_id=?",(run_id,)).fetchone()
        return json.loads(r["payload"]) if r else None
