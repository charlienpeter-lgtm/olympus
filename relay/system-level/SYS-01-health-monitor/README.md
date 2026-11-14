# SYS-01 — Health Monitor (RELAY)

## Overview

This relay bot implements the **Health Monitor** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `SYS-01`
- **Role:** Health Monitor
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Pings every bot in registry every 60 seconds. Monitors health.pong responses.

## Primary Repository

- **Repo:** https://github.com/slavox/netdata
- **Local Source Path:** ~/trading-repos/netdata

## Additional Repositories

None

## Channels

### Subscribes To:
health.pong

### Publishes To:
health.ping

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
