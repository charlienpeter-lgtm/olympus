---
trade_id: [UUID]
date: [YYYY-MM-DD]
time: [HH:MM:SS UTC]
symbol: [ES/MES/NQ/MNQ/GC/EURUSD]
direction: [Long/Short]
entry_price: [price]
exit_price: [price]
quantity: [contracts]
stop_loss: [price]
take_profit: [price]
strategy: [Strategy Name/ID]
mode: [PAPER/PROP_FIRM/LIVE]
broker: [MT5/NT8/Tradovate]
---

# Trade Journal Entry: [trade_id]

## Setup
- **Signal Source**: [Agent ID / Strategy]
- **Market Context**: [Regime, volatility, key levels]
- **Rationale**: [Why this trade made sense]
- **Conviction**: [Low/Medium/High]

## Execution
| Field | Value |
|-------|-------|
| Entry Time | [HH:MM:SS] |
| Entry Price | [price] |
| Exit Time | [HH:MM:SS] |
| Exit Price | [price] |
| Duration | [minutes/hours] |
| Slippage | [ticks] |
| Commission | [$] |

## Outcome
- **P&L**: [$]
- **R-Multiple**: [N]R
- **MAE**: [max adverse excursion]
- **MFE**: [max favorable excursion]

## Post-Trade Analysis
### What Went Well
- [Observations]

### What Could Improve
- [Observations]

### Lessons Learned
- [Key takeaways]

## Agent Trace
- Signal from: [agent]
- Juror votes: [J01-J07 results]
- R-B05 checks: [all passed/failed]
- K01 execution: [timestamp]

## Links
- Chart: [[link]]
- Backtest: [[link]]
- Agent notes: [[link]]