# XR-04 — Desks to Jurors Relay (RELAY)

## Overview

This relay bot implements the **Desks to Jurors Relay** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `XR-04`
- **Role:** Desks to Jurors Relay
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Routes messages between A (trading-desks) zone and J (jurors) zone only.

## Primary Repository

- **Repo:** https://github.com/celery/kombu
- **Local Source Path:** ~/trading-repos/kombu

## Additional Repositories

None

## Channels

### Subscribes To:
desk.analysis, trade.recommendations

### Publishes To:
juror.review

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
