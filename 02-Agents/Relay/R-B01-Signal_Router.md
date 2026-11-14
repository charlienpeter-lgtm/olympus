---
id: R-B01
role: Signal Router
status: SIMULATED_ACTIVE
trading_mode: SIMULATED
name: None
primary_repo: https://github.com/TauricResearch/TradingAgents
subscribes_to: ["signals.market", "queue.status", "priority.sorted"]
publishes_to: ["routed.signals", "queue.manage", "priority.queue", "dead.letter"]
created: 2026-11-12
---
## Role
Routes signals to appropriate downstream agents based on type, priority, and zone rules.
## Status
Current: SIMULATED_ACTIVE / SIMULATED
Name: None (pending naming system)
## Update Log
(populated by OBS)
## Notes
