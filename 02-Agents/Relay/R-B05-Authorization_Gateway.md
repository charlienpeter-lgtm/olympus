---
id: R-B05
role: Authorization Gateway
status: SIMULATED_ACTIVE
trading_mode: SIMULATED
name: None
primary_repo: https://github.com/TauricResearch/TradingAgents
subscribes_to: ["risk.signals", "veto.channel", "execution.auth"]
publishes_to: ["execution.approved", "authorization.decision", "dead.letter"]
created: 2026-11-12
---
## Role
Authorization gateway for K01. Enforces 5 checks: J01-J07 approval + A13 veto + R02 prop firm + mode + daily loss.
## Status
Current: SIMULATED_ACTIVE / SIMULATED
Name: None (pending naming system)
## Update Log
(populated by OBS)
## Notes
