"""Paced replay of an LLM driving deploy-gate-agent over MCP.

A live agent run scrolls past too fast to read, so this replays the real
sequence of tool calls at a readable cadence. run_checks reaches a separate
filesystem MCP server to confirm the change is documented. Only the pacing is
added.
"""

from __future__ import annotations

import sys
import time

from rich.console import Console
from rich.theme import Theme

THEME = Theme(
    {
        "ok": "bold #9ccfd8",
        "action": "bold #c4a7e7",
        "muted": "#6e6a86",
        "subtle": "#908caa",
        "accent": "#ebbcba",
        "prompt": "bold #f6c177",
    }
)
console = Console(theme=THEME)

PROMPT = "Ship v2.4.0 of checkout-api. Follow the change process; health check passes."
STEPS = [
    ("open_change", "service=checkout-api", "open"),
    ("run_checks", "reads CHANGELOG via filesystem MCP", "checked · documented"),
    ("approve", "approver=alice", "approved"),
    ("deploy", "version=v2.4.0", "deployed"),
    ("verify", "healthy=true", "verified"),
    ("resolve", "", "resolved"),
]


def main() -> None:
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        time.sleep(0.4)
    console.print(f"[muted](deploy-gate-agent) >[/] [prompt]{PROMPT}[/]")
    time.sleep(1.1)
    console.print()
    console.print("[subtle]the model walks the change, one enforced step at a time:[/]")
    console.print()
    time.sleep(1.0)
    for action, args, state in STEPS:
        console.print(
            f"  [subtle]→[/] [muted]step[/] [action]{action:<12}[/] [subtle]{args:<36}[/]",
            end="",
        )
        time.sleep(0.7)
        console.print(f"  [ok]✓[/]  [subtle]{state}[/]")
        time.sleep(0.85)
    console.print()
    time.sleep(0.4)
    console.print("[muted]deploy before approve was never reachable · change shipped and audited[/]")


if __name__ == "__main__":
    main()
