from agentshield.models import AgentAction, Decision
from agentshield.policies import PolicyEngine


def test_allowlist(): assert PolicyEngine().evaluate(AgentAction(tool="search"))[0] == Decision.allow
def test_shell_denied(): assert PolicyEngine().evaluate(AgentAction(tool="shell"))[0] == Decision.deny
def test_write_approval(): assert PolicyEngine().evaluate(AgentAction(tool="write_file"))[0] == Decision.approval
def test_secret_argument_denied(): assert PolicyEngine().evaluate(AgentAction(tool="search",arguments={"query":"api_key"}))[0] == Decision.deny
