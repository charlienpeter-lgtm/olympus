---
id: R-B02
role: Consensus Aggregator
status: SIMULATED_ACTIVE
trading_mode: SIMULATED
name: None
primary_repo: https://github.com/iterative/dvc
subscribes_to: ["juror.verdict", "routed.signals", "queue.status"]
publishes_to: ["consensus.decision", "queue.manage", "priority.queue", "dead.letter"]
created: 2026-11-12
---
## Role
Aggregates juror votes and consensus decisions, forwards authorized signals to execution.
## Status
Current: SIMULATED_ACTIVE / SIMULATED
Name: None (pending naming system)
## Update Log
(populated by OBS)
## Notes
