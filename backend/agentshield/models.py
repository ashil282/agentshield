from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict

def now():
    return datetime.now(timezone.utc)

class Severity(str, Enum):
    info="info"; low="low"; medium="medium"; high="high"; critical="critical"
class Decision(str, Enum):
    allow="allow"; warn="warn"; deny="deny"; approval="approval_required"

class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    category: str
    severity: Severity
    description: str
    input_text: str
    expected: str
    context: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

class AgentAction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    source: str = "simulator"
    timestamp: datetime = Field(default_factory=now)

class Finding(BaseModel):
    rule_id: str
    title: str
    severity: Severity
    description: str
    evidence: str
    action_id: str | None = None

class RunResult(BaseModel):
    run_id: str
    scenario_id: str
    status: str
    expected: str
    observed: str
    passed: bool
    score: int
    findings: list[Finding] = Field(default_factory=list)
    actions: list[AgentAction] = Field(default_factory=list)
    started_at: datetime
    finished_at: datetime
