# SYS-06 — Session Manager (RELAY)

## Overview

This relay bot implements the **Session Manager** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `SYS-06`
- **Role:** Session Manager
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Opens/closes trading sessions. Sends STANDBY or ACTIVE signal to all bots via R-B04.

## Primary Repository

- **Repo:** https://github.com/ethan-mdev/process-watch
- **Local Source Path:** ~/trading-repos/process-watch

## Additional Repositories

None

## Channels

### Subscribes To:
session.control

### Publishes To:
broadcast.system

## Inputs

Messages from upstream bots on subscribed channels.

## Outputs

Routed messages published to downstream channels.

## Requirements to Reach ACTIVE Status

1. Primary repository must be present in `~/trading-repos/` (verified by `health_check()`)
2. Relay bot code must be reviewed and validated
3. Channel routing rules must be verified against `channel_map.json`
4. Owner approval to transition from UNVERIFIED to ACTIVE
5. Trading mode remains SIMULATED unless explicitly authorized

## Notes

- This relay bot was auto-scaffolded during OLYMPUS relay layer setup.
- No dependencies were installed during setup.
- K01 (Master Execution Operator) is the only agent permitted to submit live orders.
- R-B05 is the single gateway to K01 — no exceptions.
