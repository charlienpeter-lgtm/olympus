# SYS-04 — Dead Letter Handler (RELAY)

## Overview

This relay bot implements the **Dead Letter Handler** role within the OLYMPUS trading agentic ecosystem relay layer.

- **Bot ID:** `SYS-04`
- **Role:** Dead Letter Handler
- **Bot Type:** RELAY
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

Handles undeliverable messages and dead letter queue processing.

## Primary Repository

- **Repo:** https://github.com/taskiq-python/taskiq-aio-pika
- **Local Source Path:** ~/trading-repos/taskiq-aio-pika

## Additional Repositories

None

## Channels

### Subscribes To:
dead.letter

### Publishes To:
dead.letter.handled

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
