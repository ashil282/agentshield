import re
from .models import AgentAction, Finding, Severity

RULES = [
 ("INJ-001","Instruction override attempt",Severity.high,r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions"),
 ("INJ-002","Hidden instruction extraction",Severity.high,r"(reveal|print|show|dump|repeat).{0,35}(system prompt|hidden instructions)"),
 ("EXF-001","Potential secret exfiltration",Severity.critical,r"(api[_ -]?key|password|private[_ -]?key|secret)"),
 ("TOOL-001","Command execution request",Severity.high,r"(run|execute)\s+(shell|terminal|bash|command)"),
 ("TOOL-002","External transmission request",Severity.high,r"(send|post|upload|transmit).{0,50}(external|attacker|unknown|webhook)"),
 ("EVAS-001","Encoded payload marker",Severity.medium,r"(base64|rot13|hex[_ -]?encoded|unicode escape)"),
]
def inspect_text(text):
    findings=[]
    for rid,title,sev,pattern in RULES:
        m=re.search(pattern,text,re.I)
        if m:
            evidence=text[max(0,m.start()-45):min(len(text),m.end()+65)]
            findings.append(Finding(rule_id=rid,title=title,severity=sev,
                description=f"Matched heuristic rule {rid}",evidence=evidence))
    return findings

def inspect_action(action):
    material=action.tool+" "+repr(action.arguments)
    findings=inspect_text(material)
    for f in findings: f.action_id=action.id
    if action.tool.lower() in {"shell","delete_file","send_email","http_post"}:
        findings.append(Finding(rule_id="ACT-001",title="High-impact tool invocation",
            severity=Severity.high,description="Potentially consequential tool call proposed.",
            evidence=action.tool,action_id=action.id))
    return findings
