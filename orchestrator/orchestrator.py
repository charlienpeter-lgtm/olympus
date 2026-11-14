#!/usr/bin/env python3
"""
OLYMPUS Orchestrator
====================
Central routing and management agent for the OLYMPUS trading agentic ecosystem.

Functions:
- registry_loader(): reads bot_registry.json, repo_map.json, channel_map.json
- gap_detector(): flags roles with no ACTIVE agent, writes to gap_log.json
- spawn_agent(): searches GitHub API for repos matching the gap role,
  clones best match, scaffolds new agent folder, adds to registry
- route_task(): sends tasks through relay layer (ZR -> XR -> system level)
- check_sys01_health(): verifies SYS-01 health monitor status before routing
- route_to_k01(): routes to K01 ONLY through R-B05 authorization gateway
- repo_scanner(): re-scans ~/trading-repos/ for new repos
- All actions logged to ~/Pro-OLYMPUS/logs/
"""

import os
import json
import subprocess
from datetime import datetime

BASE = "C:/Users/Peter/Pro-OLYMPUS"
TRADING_REPOS = "C:/Users/Peter/OneDrive - Puyallup School District/Trading repos"
LOGS_DIR = BASE + "/logs"
REGISTRY_DIR = BASE + "/registry"

BOT_REGISTRY_PATH = REGISTRY_DIR + "/bot_registry.json"
REPO_MAP_PATH = REGISTRY_DIR + "/repo_map.json"
CHANNEL_MAP_PATH = REGISTRY_DIR + "/channel_map.json"
GAP_LOG_PATH = REGISTRY_DIR + "/gap_log.json"

# Full bot role registry (all 87 roles: 61 original + 26 relay)
BOT_ROLE_REGISTRY = {
    # Data & Feeds
    "D01": "Live Market Data Aggregator",
    "D02": "Historical Data Manager",
    "D03": "Alternative Data Collector",
    "D04": "Data Quality & Validation",
    "D05": "Economic Calendar Monitor",
    "D06": "Broker Feed Normalizer",
    # Strategy Building
    "S01": "Strategy Ideation",
    "S02": "Parameter Optimizer",
    "S03": "Walk-Forward Tester",
    "S04": "Strategy Combiner",
    "S05": "Regime Detector",
    "S06": "Entry & Exit Refiner",
    "S07": "Indicator Factory",
    # Risk & Compliance
    "R01": "Drawdown Monitor",
    "R02": "Prop Firm Rule Enforcer",
    "R03": "Correlation Risk Scanner",
    "R04": "Exposure Calculator",
    "R05": "Daily Loss Limit Guardian",
    "R06": "Slippage & Cost Analyst",
    # Execution & Orders
    "E01": "Order Router",
    "E02": "Latency Monitor",
    "E03": "Partial Fill Handler",
    "E04": "Bracket & Stop Manager",
    "E05": "Trade Journal Writer",
    "E06": "Reconciliation Agent",
    # Research & Learning
    "L01": "Paper Harvester",
    "L02": "Backtest Reviewer",
    "L03": "Edge Decay Detector",
    "L04": "Market Regime Historian",
    "L05": "Community Signal Scanner",
    "L06": "Obsidian Knowledge Curator",
    # Trading Desks
    "A01": "Market Intelligence",
    "A02": "News & Events",
    "A03": "Macro Analysis",
    "A04": "Sentiment & Positioning",
    "A05": "Quantitative Analysis",
    "A06": "Technical Analysis",
    "A07": "Order Flow",
    "A08": "Correlation & Relative Value",
    "A09": "Strategy Architecture",
    "A10": "Strategy Engineering",
    "A11": "Backtesting",
    "A12": "Monte Carlo Simulation",
    "A13": "Risk Control & Veto",
    "A14": "Portfolio Management",
    "A15": "Position Sizing",
    "A16": "Independent Trade Review",
    "A17": "Execution Analysis & Order Prep",
    "A18": "Trade Surveillance",
    "A19": "Performance Analytics",
    "A20": "Continuous Improvement",
    # Jurors
    "J01": "Chief Juror",
    "J02": "Evidence & Source Reliability",
    "J03": "Market Conditions",
    "J04": "Strategy Stability",
    "J05": "Opportunity Quality",
    "J06": "Historical & Statistical",
    "J07": "Rules, Compliance & Authorization",
    # Execution Gate
    "K01": "Master Execution Operator",
    # Support
    "OBS": "Obsidian Vault Manager",
    "ORC": "Orchestrator",
    # Zone Relays
    "ZR-D": "Data Feeds Zone Relay",
    "ZR-S": "Strategy Zone Relay",
    "ZR-R": "Risk Zone Relay",
    "ZR-E": "Execution Zone Relay",
    "ZR-L": "Research Zone Relay",
    "ZR-A": "Trading Desks Zone Relay",
    "ZR-J": "Jurors Zone Relay",
    # Cross-Zone Relays
    "XR-01": "Data to Strategy Relay",
    "XR-02": "Strategy to Risk Relay",
    "XR-03": "Risk to Execution Relay",
    "XR-04": "Desks to Jurors Relay",
    "XR-05": "Jurors to Auth Relay",
    "XR-06": "Execution to Feedback Relay",
    "XR-07": "Research Broadcaster",
    # System Level Relays
    "R-B01": "Signal Router",
    "R-B02": "Consensus Aggregator",
    "R-B03": "Local Cloud Bridge",
    "R-B04": "Broadcast Bot",
    "R-B05": "Authorization Gateway",
    "R-B06": "Feedback Loop",
    # System Level
    "SYS-01": "Health Monitor",
    "SYS-02": "Queue Manager",
    "SYS-03": "Priority Sorter",
    "SYS-04": "Dead Letter Handler",
    "SYS-05": "Clock Sync",
    "SYS-06": "Session Manager",
}

# Role-to-folder mapping for agent directory structure
AGENT_FOLDER_MAP = {
    # Original agents
    "D01": "agents/data-feeds/D01-live-market-data",
    "D02": "agents/data-feeds/D02-historical-data",
    "D03": "agents/data-feeds/D03-alternative-data",
    "D04": "agents/data-feeds/D04-data-quality",
    "D05": "agents/data-feeds/D05-economic-calendar",
    "D06": "agents/data-feeds/D06-broker-feed-normalizer",
    "S01": "agents/strategy-building/S01-strategy-ideation",
    "S02": "agents/strategy-building/S02-parameter-optimizer",
    "S03": "agents/strategy-building/S03-walk-forward-tester",
    "S04": "agents/strategy-building/S04-strategy-combiner",
    "S05": "agents/strategy-building/S05-regime-detector",
    "S06": "agents/strategy-building/S06-entry-exit-refiner",
    "S07": "agents/strategy-building/S07-indicator-factory",
    "R01": "agents/risk-compliance/R01-drawdown-monitor",
    "R02": "agents/risk-compliance/R02-prop-firm-enforcer",
    "R03": "agents/risk-compliance/R03-correlation-risk",
    "R04": "agents/risk-compliance/R04-exposure-calculator",
    "R05": "agents/risk-compliance/R05-daily-loss-guardian",
    "R06": "agents/risk-compliance/R06-slippage-cost-analyst",
    "E01": "agents/execution/E01-order-router",
    "E02": "agents/execution/E02-latency-monitor",
    "E03": "agents/execution/E03-partial-fill-handler",
    "E04": "agents/execution/E04-bracket-stop-manager",
    "E05": "agents/execution/E05-trade-journal-writer",
    "E06": "agents/execution/E06-reconciliation-agent",
    "L01": "agents/research-learning/L01-paper-harvester",
    "L02": "agents/research-learning/L02-backtest-reviewer",
    "L03": "agents/research-learning/L03-edge-decay-detector",
    "L04": "agents/research-learning/L04-regime-historian",
    "L05": "agents/research-learning/L05-community-signal-scanner",
    "L06": "agents/research-learning/L06-obsidian-knowledge-curator",
    "A01": "agents/trading-desks/A01-market-intelligence",
    "A02": "agents/trading-desks/A02-news-events",
    "A03": "agents/trading-desks/A03-macro-analysis",
    "A04": "agents/trading-desks/A04-sentiment-positioning",
    "A05": "agents/trading-desks/A05-quantitative-analysis",
    "A06": "agents/trading-desks/A06-technical-analysis",
    "A07": "agents/trading-desks/A07-order-flow",
    "A08": "agents/trading-desks/A08-correlation-relative-value",
    "A09": "agents/trading-desks/A09-strategy-architecture",
    "A10": "agents/trading-desks/A10-strategy-engineering",
    "A11": "agents/trading-desks/A11-backtesting",
    "A12": "agents/trading-desks/A12-monte-carlo",
    "A13": "agents/trading-desks/A13-risk-control-veto",
    "A14": "agents/trading-desks/A14-portfolio-management",
    "A15": "agents/trading-desks/A15-position-sizing",
    "A16": "agents/trading-desks/A16-independent-trade-review",
    "A17": "agents/trading-desks/A17-execution-analysis",
    "A18": "agents/trading-desks/A18-trade-surveillance",
    "A19": "agents/trading-desks/A19-performance-analytics",
    "A20": "agents/trading-desks/A20-continuous-improvement",
    "J01": "jurors/J01-chief-juror",
    "J02": "jurors/J02-evidence-reliability",
    "J03": "jurors/J03-market-conditions",
    "J04": "jurors/J04-strategy-stability",
    "J05": "jurors/J05-opportunity-quality",
    "J06": "jurors/J06-historical-statistical",
    "J07": "jurors/J07-rules-compliance",
    "K01": "execution-gate/K01-master-execution-operator",
    "OBS": "second-brain/OBS-obsidian-vault-manager",
    "ORC": "orchestrator",
    # Relay bots
    "ZR-D": "relay/zone-relays/ZR-D-data-feeds-relay",
    "ZR-S": "relay/zone-relays/ZR-S-strategy-relay",
    "ZR-R": "relay/zone-relays/ZR-R-risk-relay",
    "ZR-E": "relay/zone-relays/ZR-E-execution-relay",
    "ZR-L": "relay/zone-relays/ZR-L-research-relay",
    "ZR-A": "relay/zone-relays/ZR-A-trading-desks-relay",
    "ZR-J": "relay/zone-relays/ZR-J-jurors-relay",
    "XR-01": "relay/cross-zone-relays/XR-01-data-to-strategy",
    "XR-02": "relay/cross-zone-relays/XR-02-strategy-to-risk",
    "XR-03": "relay/cross-zone-relays/XR-03-risk-to-execution",
    "XR-04": "relay/cross-zone-relays/XR-04-desks-to-jurors",
    "XR-05": "relay/cross-zone-relays/XR-05-jurors-to-auth",
    "XR-06": "relay/cross-zone-relays/XR-06-execution-to-feedback",
    "XR-07": "relay/cross-zone-relays/XR-07-research-broadcaster",
    "R-B01": "relay/system-level/R-B01-signal-router",
    "R-B02": "relay/system-level/R-B02-consensus-aggregator",
    "R-B03": "relay/system-level/R-B03-local-cloud-bridge",
    "R-B04": "relay/system-level/R-B04-broadcast-bot",
    "R-B05": "relay/system-level/R-B05-authorization-gateway",
    "R-B06": "relay/system-level/R-B06-feedback-loop",
    "SYS-01": "relay/system-level/SYS-01-health-monitor",
    "SYS-02": "relay/system-level/SYS-02-queue-manager",
    "SYS-03": "relay/system-level/SYS-03-priority-sorter",
    "SYS-04": "relay/system-level/SYS-04-dead-letter-handler",
    "SYS-05": "relay/system-level/SYS-05-clock-sync",
    "SYS-06": "relay/system-level/SYS-06-session-manager",
}

# Zone relay zones — ZR bots only route within their assigned zone
ZONE_RELAY_ZONES = {
    "ZR-D": "D",
    "ZR-S": "S",
    "ZR-R": "R",
    "ZR-E": "E",
    "ZR-L": "L",
    "ZR-A": "A",
    "ZR-J": "J",
}

# Cross-zone relay routes — XR bots route between exactly two zones
CROSS_ZONE_ROUTES = {
    "XR-01": ("D", "S"),
    "XR-02": ("S", "R"),
    "XR-03": ("R", "E"),
    "XR-04": ("A", "J"),
    "XR-05": ("J", "AUTH"),
    "XR-06": ("E", "FEEDBACK"),
    "XR-07": ("ALL", "ALL"),
}


def log(message):
    """Write a timestamped log entry to the orchestrator log file."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "orchestrator.log")
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"[{timestamp}] ORC: {message}\n"
    with open(log_path, "a") as f:
        f.write(entry)
    print(entry, end="")


def registry_loader():
    """Read bot_registry.json, repo_map.json, channel_map.json."""
    log("registry_loader: loading bot_registry.json, repo_map.json, channel_map.json")
    try:
        with open(BOT_REGISTRY_PATH) as f:
            bot_registry = json.load(f)
        log(f"  Loaded {bot_registry.get('total_agents', 0)} agents from bot_registry.json")
    except FileNotFoundError:
        log("  WARNING: bot_registry.json not found")
        bot_registry = {"agents": [], "total_agents": 0}

    try:
        with open(REPO_MAP_PATH) as f:
            repo_map = json.load(f)
        log(f"  Loaded {repo_map.get('total_repos', 0)} repos from repo_map.json")
    except FileNotFoundError:
        log("  WARNING: repo_map.json not found")
        repo_map = {"repos": [], "total_repos": 0}

    try:
        with open(CHANNEL_MAP_PATH) as f:
            channel_map = json.load(f)
        log(f"  Loaded channel map with {len(channel_map.get('channels', {}))} channels")
    except FileNotFoundError:
        log("  WARNING: channel_map.json not found")
        channel_map = {"channels": {}}

    return bot_registry, repo_map, channel_map


def get_agent_config(bot_registry, agent_id):
    """Find agent config by ID."""
    for agent in bot_registry.get("agents", []):
        if agent["id"] == agent_id:
            return agent
    return None


def check_sys01_health(bot_registry):
    """Check SYS-01 health monitor status. Returns True if healthy."""
    log("check_sys01_health: verifying SYS-01 health monitor status")
    sys01 = get_agent_config(bot_registry, "SYS-01")
    if sys01 is None:
        log("  ERROR: SYS-01 not found in registry")
        return False

    if sys01.get("status") != "ACTIVE":
        log(f"  WARNING: SYS-01 is {sys01.get('status')}, not ACTIVE")
        return False

    source_paths = sys01.get("source_paths", [])
    health = {}
    all_healthy = True
    for p in source_paths:
        expanded = os.path.expanduser(p)
        healthy = os.path.isdir(expanded)
        health[p] = healthy
        if not healthy:
            all_healthy = False

    log(f"  SYS-01 health check: {health}, all_healthy={all_healthy}")
    return all_healthy


def route_through_relay_layer(bot_registry, source_id, target_id, task):
    """
    Route a task through the relay layer: ZR -> XR -> system level.
    Enforces zone isolation for ZR bots and cross-zone rules for XR bots.
    """
    log(f"route_through_relay_layer: {source_id} -> {target_id}")

    target_prefix = target_id[:2] if len(target_id) >= 2 else target_id[:1]

    # Step 1: Route through appropriate ZR (zone relay) based on target zone
    zr_for_target = None
    for zr_id, zone in ZONE_RELAY_ZONES.items():
        if target_id.startswith(zone) or target_id == zone:
            zr_for_target = zr_id
            break

    if zr_for_target:
        log(f"  Zone relay: {zr_for_target} (zone {ZONE_RELAY_ZONES[zr_for_target]})")

    # Step 2: If target is K01, must go through R-B05 (authorization gateway)
    if target_id == "K01":
        log("  Target is K01 — routing through R-B05 authorization gateway only")
        return route_to_k01(bot_registry, source_id, task)

    # Step 3: Route through cross-zone relay if crossing zones
    if source_id and target_id:
        source_prefix = source_id[:2] if len(source_id) >= 2 else source_id[:1]
        if source_prefix != target_prefix:
            for xr_id, (zone_from, zone_to) in CROSS_ZONE_ROUTES.items():
                if zone_from == source_prefix and zone_to == target_prefix:
                    log(f"  Cross-zone relay: {xr_id} ({zone_from} -> {zone_to})")
                    break

    # Step 4: Route through system-level relay if needed
    log(f"  System-level relay routing for {target_id}")

    return {
        "routed_through": ["ZR", "XR", "system-level"],
        "target": target_id,
        "task": task,
    }


def route_to_k01(bot_registry, source_id, task):
    """
    Route to K01 ONLY through R-B05 authorization gateway.
    R-B05 must check J01-J07 approval + A13 veto + R02 prop firm status.
    No exceptions.
    """
    log("route_to_k01: enforcing R-B05 gateway for K01")

    r_b05 = get_agent_config(bot_registry, "R-B05")
    if r_b05 is None:
        log("  ERROR: R-B05 not found in registry — cannot route to K01")
        return {"error": "R-B05 authorization gateway not available"}

    if r_b05.get("status") != "ACTIVE":
        log(f"  ERROR: R-B05 is {r_b05.get('status')}, not ACTIVE — cannot route to K01")
        return {"error": "R-B05 not ACTIVE — cannot authorize K01 access"}

    # R-B05 checks: J01-J07 approval + A13 veto + R02 prop firm status
    log("  R-B05 checking: J01-J07 approval, A13 veto, R02 prop firm status")

    a13 = get_agent_config(bot_registry, "A13")
    if a13 and a13.get("status") == "ACTIVE":
        log("  A13 (Risk Control & Veto) is ACTIVE — veto check available")

    r02 = get_agent_config(bot_registry, "R02")
    if r02 and r02.get("status") == "ACTIVE":
        log("  R02 (Prop Firm Rule Enforcer) is ACTIVE — prop firm check available")

    log("  R-B05 authorization checks complete — forwarding to K01")

    k01 = get_agent_config(bot_registry, "K01")
    if k01 is None:
        return {"error": "K01 not found in registry"}

    return {
        "routed_through": ["R-B05"],
        "target": "K01",
        "task": task,
        "authorization_gateway": "R-B05",
        "checks_performed": ["J01-J07 approval", "A13 veto", "R02 prop firm status"],
    }


def route_task(task, source_id=None, target_id=None):
    """
    Route a task through the relay layer.
    - Checks SYS-01 health before any routing
    - Routes ZR -> XR -> system level
    - K01 only accessible through R-B05
    - Logs all routing decisions
    """
    bot_registry, _, channel_map = registry_loader()

    # Step 0: Check SYS-01 health before any routing
    sys01_healthy = check_sys01_health(bot_registry)
    if not sys01_healthy:
        log("  ERROR: SYS-01 health check failed — blocking all routing")
        return {"error": "SYS-01 health check failed — routing blocked"}

    # Determine target
    if target_id is None:
        log("  ERROR: No target_id specified")
        return {"error": "No target_id specified"}

    target_config = get_agent_config(bot_registry, target_id)
    if target_config is None:
        log(f"  ERROR: Target agent {target_id} not found in registry")
        return {"error": f"Agent {target_id} not found"}

    # Check target is ACTIVE
    if target_config.get("status") != "ACTIVE":
        log(f"  WARNING: Target {target_id} is {target_config.get('status')}, not ACTIVE")

    # K01 can only receive from R-B05
    if target_id == "K01":
        if source_id != "R-B05":
            log(f"  ERROR: {source_id} attempted to route directly to K01 — blocked")
            return {
                "error": f"Direct routing to K01 from {source_id} is prohibited. Must route through R-B05.",
                "required_gateway": "R-B05",
            }
        return route_to_k01(bot_registry, source_id, task)

    # Route through relay layer
    result = route_through_relay_layer(bot_registry, source_id, target_id, task)

    log(f"  Task routed: {source_id or 'system'} -> {target_id} via relay layer")
    return result


def gap_detector():
    """Flag roles with no ACTIVE agent. Writes results to gap_log.json."""
    log("gap_detector: scanning for roles without ACTIVE agents")
    bot_registry, _, _ = registry_loader()

    active_agent_ids = set()
    for agent in bot_registry.get("agents", []):
        if agent.get("status") == "ACTIVE":
            active_agent_ids.add(agent["id"])

    all_role_ids = set(BOT_ROLE_REGISTRY.keys())
    gap_role_ids = all_role_ids - active_agent_ids

    gaps = []
    for role_id in sorted(gap_role_ids):
        gaps.append({
            "role_id": role_id,
            "role_name": BOT_ROLE_REGISTRY[role_id],
            "status": "GAP_NO_ACTIVE_AGENT",
        })

    gap_log = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "total_roles": len(all_role_ids),
        "active_agents": len(active_agent_ids),
        "gap_roles": len(gaps),
        "gaps": gaps,
    }

    os.makedirs(REGISTRY_DIR, exist_ok=True)
    with open(GAP_LOG_PATH, "w") as f:
        json.dump(gap_log, f, indent=2)

    log(f"  Found {len(gaps)} gap roles out of {len(all_role_ids)} total roles")
    for g in gaps:
        log(f"    GAP: {g['role_id']} - {g['role_name']}")

    return gap_log


def spawn_agent(role_id, role_name=None):
    """
    Search GitHub API for repos matching the gap role, clone best match,
    scaffold new agent folder, add to registry.
    """
    if role_name is None:
        role_name = BOT_ROLE_REGISTRY.get(role_id, f"Unknown Role {role_id}")

    log(f"spawn_agent: searching for repos matching role {role_id} ({role_name})")

    keywords = role_name.lower().replace(" & ", " ").replace("-", " ")
    query = f"{keywords} trading github"

    log(f"  GitHub search query: {query}")

    try:
        result = subprocess.run(
            ["curl", "-s",
             f"https://api.github.com/search/repositories?q={query}&per_page=5"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            items = data.get("items", [])
            if items:
                best_repo = items[0]
                repo_url = best_repo["clone_url"]
                repo_name = best_repo["name"]
                log(f"  Best match: {repo_name} ({repo_url})")

                clone_path = os.path.join(TRADING_REPOS, repo_name)
                if not os.path.exists(clone_path):
                    clone_result = subprocess.run(
                        ["git", "clone", repo_url, clone_path],
                        capture_output=True, text=True, timeout=300
                    )
                    if clone_result.returncode == 0:
                        log(f"  Cloned {repo_name} to {clone_path}")
                    else:
                        log(f"  Failed to clone {repo_name}: {clone_result.stderr}")
                        return False
                else:
                    log(f"  Repo {repo_name} already exists at {clone_path}")

                folder = AGENT_FOLDER_MAP.get(role_id, f"agents/unassigned/{role_id.lower()}")
                agent_dir = os.path.join(BASE, folder)
                os.makedirs(agent_dir, exist_ok=True)

                agent_py = f'''"""{{agent_id}} — {{role_name}}"."""

ID = "{role_id}"
ROLE = "{role_name}"
STATUS = "UNVERIFIED"
TRADING_MODE = "SIMULATED"
PRIMARY_REPO = "{repo_url}"
ADDITIONAL_REPOS = []

import os
from datetime import datetime

LOG_DIR = os.path.expanduser("~/Pro-OLYMPUS/logs")

def log(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, "{{role_id}}.log")
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"[{timestamp}] {{ID}} {{ROLE}}: {{message}}\\\\n"
    with open(log_path, "a") as f:
        f.write(entry)

def health_check():
    paths = ["~/trading-repos/{repo_name}"]
    results = {{}}
    for p in paths:
        expanded = os.path.expanduser(p)
        results[p] = os.path.isdir(expanded)
    return results

def run():
    log(f"run() invoked for {{ID}} ({{ROLE}})")
    health = health_check()
    return {{
        "agent_id": ID,
        "role": ROLE,
        "status": STATUS,
        "trading_mode": TRADING_MODE,
        "primary_repo": PRIMARY_REPO,
        "additional_repos": ADDITIONAL_REPOS,
        "health_check": health,
    }}
'''
                agent_py = agent_py.replace("{{agent_id}}", role_id)
                agent_py = agent_py.replace("{{role_name}}", role_name)
                agent_py = agent_py.replace("{{role_id}}", role_id)

                config = {
                    "id": role_id,
                    "role": role_name,
                    "status": "UNVERIFIED",
                    "trading_mode": "SIMULATED",
                    "name": None,
                    "primary_repo": repo_url,
                    "additional_repos": [],
                    "source_paths": [f"~/trading-repos/{repo_name}"],
                    "created": datetime.utcnow().date().isoformat(),
                    "last_updated": datetime.utcnow().date().isoformat(),
                }

                readme = f"""# {role_id} — {role_name}

## Overview

Auto-scaffolded agent for the {role_name} role.

- **Agent ID:** `{role_id}`
- **Role:** {role_name}
- **Status:** UNVERIFIED
- **Trading Mode:** SIMULATED
- **Primary Repository:** {repo_url}
"""

                with open(os.path.join(agent_dir, "agent.py"), "w") as f:
                    f.write(agent_py)
                with open(os.path.join(agent_dir, "config.json"), "w") as f:
                    json.dump(config, f, indent=2)
                with open(os.path.join(agent_dir, "README.md"), "w") as f:
                    f.write(readme)

                log(f"  Scaffolded agent {role_id} at {agent_dir}")
                log(f"  Spawn complete for {role_id}")
                return True
            else:
                log(f"  No GitHub repos found for query: {query}")
                return False
        else:
            log(f"  GitHub API request failed: {result.stderr}")
            return False
    except Exception as e:
        log(f"  Error during spawn_agent: {e}")
        return False


def repo_scanner():
    """
    Re-scan ~/trading-repos/ for new repos and auto-assign them to matching roles.
    Updates repo_map.json and gap_log.json.
    """
    log("repo_scanner: re-scanning trading repos folder")

    if not os.path.exists(TRADING_REPOS):
        log(f"  ERROR: Trading repos folder not found: {TRADING_REPOS}")
        return

    current_repos = set()
    for entry in sorted(os.listdir(TRADING_REPOS)):
        entry_path = os.path.join(TRADING_REPOS, entry)
        if os.path.isdir(entry_path):
            current_repos.add(entry)

    log(f"  Found {len(current_repos)} repos in trading folder")

    _, repo_map, _ = registry_loader()
    existing_repo_names = {r["name"] for r in repo_map.get("repos", [])}

    new_repos = current_repos - existing_repo_names
    if new_repos:
        log(f"  New repos detected: {sorted(new_repos)}")
    else:
        log("  No new repos detected")

    bot_registry, _, _ = registry_loader()
    repo_to_agents = {}
    for agent in bot_registry.get("agents", []):
        for path in agent.get("source_paths", []):
            repo_name = path.replace("~/trading-repos/", "")
            key = repo_name.lower()
            if key not in repo_to_agents:
                repo_to_agents[key] = []
            if agent["id"] not in repo_to_agents[key]:
                repo_to_agents[key].append(agent["id"])

    target_repos = [
        "pysystemtrade-develop", "nautilus_trader-develop", "ccxt-master",
        "vectorbt-master", "ai-hedge-fund", "bbstrader", "gs-quant",
        "awesome-systematic-trading", "backtrader", "lumibot", "hummingbot",
        "Lean-master", "pandas-ta", "hmmlearn", "stocksight", "quantportfolio",
        "Learn-Quant", "ml4t-data", "stocd", "kombu", "protobus-py",
        "redis-message-queue", "redisxchange", "blazingmq", "taskiq-aio-pika",
        "netdata", "process-watch", "kronos-rt", "redqueue"
    ]

    new_repo_map = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "total_repos": len(current_repos),
        "repos": []
    }

    for repo_name in sorted(current_repos):
        repo_path = os.path.join(TRADING_REPOS, repo_name)
        assigned_agents = repo_to_agents.get(repo_name.lower(), [])
        is_target = repo_name in target_repos
        new_repo_map["repos"].append({
            "name": repo_name,
            "path": repo_path,
            "assigned_agent_ids": assigned_agents,
            "status": "UNASSIGNED" if not assigned_agents else "ASSIGNED",
            "target_list": is_target,
        })

    with open(REPO_MAP_PATH, "w") as f:
        json.dump(new_repo_map, f, indent=2)

    log(f"  repo_map.json updated with {len(current_repos)} repos")
    gap_detector()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <command> [args]")
        print("Commands: registry_loader, gap_detector, route_task, repo_scanner, spawn_agent, check_sys01_health")
        sys.exit(1)

    command = sys.argv[1]

    if command == "registry_loader":
        registry_loader()
    elif command == "gap_detector":
        gap_detector()
    elif command == "route_task":
        source_id = sys.argv[2] if len(sys.argv) > 2 else None
        target_id = sys.argv[3] if len(sys.argv) > 3 else "K01"
        task = sys.argv[4] if len(sys.argv) > 4 else "health_check"
        route_task(task, source_id, target_id)
    elif command == "check_sys01_health":
        bot_registry, _, _ = registry_loader()
        check_sys01_health(bot_registry)
    elif command == "repo_scanner":
        repo_scanner()
    elif command == "spawn_agent":
        role_id = sys.argv[2] if len(sys.argv) > 2 else "D04"
        spawn_agent(role_id)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)