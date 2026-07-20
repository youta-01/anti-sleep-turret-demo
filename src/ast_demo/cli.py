from __future__ import annotations

import argparse
import json

from .scenarios import SCENARIOS
from .state_machine import AstDemo


def run_headless(name: str) -> dict[str, object]:
    app = AstDemo()
    SCENARIOS[name](app)
    return {
        "scenario": name,
        "state": app.status.state.value,
        "risk": round(app.status.risk, 1),
        "risk_reason": app.status.risk_reason,
        "risk_episodes": len(app.guard.episodes),
        "intervention_source": app.status.intervention_source.value,
        "riz_active": app.status.riz_active,
        "transitions": len(app.status.history),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Anti-Sleep Turret public demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="monitoring")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args(argv)
    if args.headless:
        print(json.dumps(run_headless(args.scenario), ensure_ascii=False, sort_keys=True))
        return 0
    from .ui import launch

    launch(args.scenario)
    return 0
