# J07 — Rules, Compliance & Authorization

## Overview

This agent implements the **Rules, Compliance & Authorization** role within the OLYMPUS trading agentic ecosystem.

- **Agent ID:** `J07`
- **Role:** Rules, Compliance & Authorization
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED

## Primary Repository

- **Repo:** Not yet assigned
- **Local Source Path:** Not yet cloned

## Additional Repositories

None

## Inputs

This agent expects:
- Market data and signals from upstream data-feed agents (D-series)
- Strategy proposals from strategy-building agents (S-series)
- Risk assessments from risk-compliance agents (R-series)

## Outputs

This agent produces:
- Role-specific analysis and recommendations
- Health check reports on source repository availability
- Log entries written to `~/Pro-OLYMPUS/logs/J07.log`

## Requirements to Reach ACTIVE Status

1. Primary repository must be present in `~/trading-repos/` (verified by `health_check()`)
2. Agent code must be reviewed and validated against its assigned role
3. Integration tests must pass with the orchestrator
4. Owner approval to transition from UNVERIFIED to ACTIVE
5. Trading mode remains SIMULATED unless explicitly authorized for live operation

## Notes

- This agent was auto-scaffolded during OLYMPUS setup (Step 5).
- No dependencies were installed during setup.
- K01 (Master Execution Operator) is the only agent permitted to submit live orders.
