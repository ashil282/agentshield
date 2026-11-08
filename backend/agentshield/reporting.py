from pathlib import Path


def esc(v):
    return str(v).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#x27;")
def to_json(result):
    return result.model_dump_json(indent=2)
def to_html(result):
    rows="".join(f"<tr><td>{esc(f.rule_id)}</td><td>{esc(f.severity.value)}</td><td>{esc(f.title)}</td><td><code>{esc(f.evidence)}</code></td></tr>" for f in result.findings)
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>AgentShield report</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:3rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccd;padding:.6rem;text-align:left}}</style>
<h1>AgentShield security report</h1><p>Run {esc(result.run_id)}</p><h2>Risk score: {result.score}/100</h2>
<p>Scenario {esc(result.scenario_id)} · expected {esc(result.expected)} · observed {esc(result.observed)} · passed {result.passed}</p>
<table><tr><th>Rule</th><th>Severity</th><th>Finding</th><th>Evidence</th></tr>{rows}</table></html>'''
def write_report(result,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(to_html(result) if p.suffix.lower()==".html" else to_json(result),encoding="utf-8")
    return p
