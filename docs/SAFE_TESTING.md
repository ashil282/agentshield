# Safe testing rules
- Use bundled synthetic scenarios or systems you own and are authorized to assess.
- Never paste real API keys, passwords, private keys, customer data or confidential prompts.
- Do not add arbitrary command execution or live network dispatch to the simulator without a separate threat model and sandbox review.
- Keep the API on `127.0.0.1`; v1 has no authentication.
- Review evidence excerpts before sharing reports.
- Passing means the deterministic expected outcome matched; it does not prove a deployed agent is safe.
