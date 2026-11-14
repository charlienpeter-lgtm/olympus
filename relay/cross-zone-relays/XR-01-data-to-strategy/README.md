# XR-01 — Data to Strategy Relay (RELAY)

## Overview

This relay bot implements the **Data to Strategy Relay** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `XR-01`
- **Role:** Data to Strategy Relay
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Routes messages between D (data-feeds) zone and S (strategy-building) zone only.

## Primary Repository

- **Repo:** https://github.com/celery/kombu
- **Local Source Path:** ~/trading-repos/kombu

## Additional Repositories

None

## Channels

### Subscribes To:
signals.market

### Publishes To:
strategy.inputs

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
