---
id: SYS-03
role: Priority Sorter
status: SIMULATED_ACTIVE
trading_mode: SIMULATED
name: None
primary_repo: https://github.com/ArielLaub/protobus-py
subscribes_to: ["priority.queue"]
publishes_to: ["priority.sorted", "dead.letter"]
created: 2026-11-12
---
## Role
Sorts messages by priority (risk alerts > trade signals > research) before routing.
## Status
Current: SIMULATED_ACTIVE / SIMULATED
Name: None (pending naming system)
## Update Log
(populated by OBS)
## Notes
