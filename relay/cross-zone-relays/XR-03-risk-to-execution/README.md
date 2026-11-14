# XR-03 — Risk to Execution Relay (RELAY)

## Overview

This relay bot implements the **Risk to Execution Relay** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `XR-03`
- **Role:** Risk to Execution Relay
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Routes messages between R (risk-compliance) zone and E (execution) zone only.

## Primary Repository

- **Repo:** https://github.com/TauricResearch/TradingAgents
- **Local Source Path:** ~/trading-repos/Trading-Agents/bot-0028

## Additional Repositories

None

## Channels

### Subscribes To:
risk.signals

### Publishes To:
execution.approved

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
