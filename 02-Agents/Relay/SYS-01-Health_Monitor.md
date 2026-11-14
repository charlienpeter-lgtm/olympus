---
id: SYS-01
role: Health Monitor
status: SIMULATED_ACTIVE
trading_mode: SIMULATED
name: None
primary_repo: https://github.com/slavox/netdata
subscribes_to: ["health.pong"]
publishes_to: ["system.alerts", "health.ping", "dead.letter"]
created: 2026-11-12
---
## Role
Monitors agent health via heartbeat pings, marks offline agents, publishes periodic health pings.
## Status
Current: SIMULATED_ACTIVE / SIMULATED
Name: None (pending naming system)
## Update Log
(populated by OBS)
## Notes
