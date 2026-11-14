---
backtest_id: [UUID]
strategy_id: [STRAT-NNN]
strategy_version: [vX.Y]
date: [YYYY-MM-DD]
mode: [PAPER/PROP_FIRM/LIVE]
---

# Backtest Report: [Strategy Name] v[X.Y]

## Configuration
| Parameter | Value |
|-----------|-------|
| Symbols | [ES, MES, NQ, MNQ, GC, EURUSD] |
| Timeframes | [1m, 5m, 15m, 1h, 4h, 1d] |
| Period | [Start Date] to [End Date] |
| Data Source | [MT5/NT8/Tradovate/Combined] |
| Commission | [$X per contract] |
| Slippage Model | [X ticks / % of spread] |

## In-Sample Results
| Metric | Value |
|--------|-------|
| Total Return | [%] |
| Annualized Return | [%] |
| Sharpe Ratio | |
| Sortino Ratio | |
| Calmar Ratio | |
| Max Drawdown | [%] |
| Win Rate | [%] |
| Profit Factor | |
| Avg Trade | [$] |
| Total Trades | [N] |

## Out-of-Sample Results
| Metric | Value |
|--------|-------|
| Total Return | [%] |
| Sharpe Ratio | |
| Max Drawdown | [%] |
| Win Rate | [%] |

## Monte Carlo Simulation
- **Runs**: [10,000]
- **Seed**: [12345]
- **5th Percentile Return**: [%]
- **Median Return**: [%]
- **95th Percentile Return**: [%]
- **Probability of Ruin**: [%]
- **Max DD 5th percentile**: [%]

## Walk-Forward Analysis
| Window | Train Period | Test Period | Return | Sharpe | Max DD |
|--------|--------------|-------------|--------|--------|--------|
| 1 | [dates] | [dates] | [%] | | [%] |
| 2 | [dates] | [dates] | [%] | | [%] |
| ... | ... | ... | ... | ... | ... |

## Parameter Stability
| Parameter | Optimal | Range Tested | Sensitivity |
|-----------|---------|--------------|-------------|
| [param1] | [val] | [min-max] | [Low/Med/High] |

## Risk Metrics
- Max Positions: [N]
- Max Daily Loss: [$]
- Correlation Limit: [description]
- Prop Firm Compliant: [Y/N]

## Conclusion
- **Status**: [APPROVED / REJECTED / NEEDS REFINEMENT]
- **Notes**: [Key findings, caveats, next steps]

## Artifacts
- Equity Curve: [[link]]
- Trade List: [[link]]
- Monte Carlo Distribution: [[link]]
- Parameter Heatmap: [[link]]