# R-B05 — Authorization Gateway (RELAY)

## Overview

This relay bot implements the **Authorization Gateway** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `R-B05`
- **Role:** Authorization Gateway
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Single gateway to K01. Must check J01-J07 approval + A13 veto + R02 prop firm status before passing ANY message to K01.

## Primary Repository

- **Repo:** https://github.com/TauricResearch/TradingAgents
- **Local Source Path:** ~/trading-repos/Trading-Agents/bot-0027

## Additional Repositories

None

## Channels

### Subscribes To:
execution.auth, risk.signals, veto.channel

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
