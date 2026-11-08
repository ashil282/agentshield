from .models import AgentAction
class SimulatedAgent:
    """Deterministic simulator. Never executes processes, writes files, or accesses networks."""
    def propose(self, scenario):
        text=scenario.input_text.lower()
        actions=[]
        if any(x in text for x in ("send","upload","exfiltrate","transmit")):
            actions.append(AgentAction(tool="http_post",arguments={"destination":"https://example.invalid","payload":"synthetic-placeholder"}))
        if "delete" in text or "remove all files" in text:
            actions.append(AgentAction(tool="delete_file",arguments={"path":"/tmp/synthetic.txt"}))
        if any(x in text for x in ("run shell","execute bash","terminal command")):
            actions.append(AgentAction(tool="shell",arguments={"command":"echo synthetic"}))
        if "write file" in text or "save report" in text:
            actions.append(AgentAction(tool="write_file",arguments={"path":"sandbox/report.txt","content":"synthetic"}))
        if not actions: actions.append(AgentAction(tool="search",arguments={"query":"safe synthetic lookup"}))
        return actions
