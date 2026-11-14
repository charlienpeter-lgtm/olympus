# XR-07 — Research Broadcaster (RELAY)

## Overview

This relay bot implements the **Research Broadcaster** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `XR-07`
- **Role:** Research Broadcaster
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Broadcasts research findings across all zones via the system broadcast channel.

## Primary Repository

- **Repo:** https://github.com/elijas/redis-message-queue
- **Local Source Path:** ~/trading-repos/redis-message-queue

## Additional Repositories

~/trading-repos/protobus-py

## Channels

### Subscribes To:
research.findings

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
