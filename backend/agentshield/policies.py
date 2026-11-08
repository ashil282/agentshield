from dataclasses import dataclass, field
from .models import AgentAction, Decision

@dataclass
class Policy:
    name: str = "default"
    allowed_tools: set[str] = field(default_factory=lambda: {"search","calculator","read_public"})
    denied_tools: set[str] = field(default_factory=lambda: {"shell","delete_file","send_email","http_post"})
    require_approval: set[str] = field(default_factory=lambda: {"write_file","http_get"})
    blocked_argument_terms: tuple[str,...] = ("password","api_key","secret_value","private_key")

class PolicyEngine:
    def __init__(self, policy=None):
        self.policy = policy or Policy()
    def evaluate(self, action: AgentAction):
        tool = action.tool.lower().strip()
        if tool in self.policy.denied_tools:
            return Decision.deny, f"Tool '{tool}' is explicitly denied"
        if tool in self.policy.require_approval:
            return Decision.approval, f"Tool '{tool}' requires human approval"
        if tool not in self.policy.allowed_tools:
            return Decision.deny, f"Tool '{tool}' is not allowlisted"
        if any(term in repr(action.arguments).lower() for term in self.policy.blocked_argument_terms):
            return Decision.deny, "Arguments contain a protected-data marker"
        return Decision.allow, "Tool and arguments satisfy policy"
    def as_dict(self):
        return {"name":self.policy.name,"allowed_tools":sorted(self.policy.allowed_tools),
                "denied_tools":sorted(self.policy.denied_tools),
                "require_approval":sorted(self.policy.require_approval)}
