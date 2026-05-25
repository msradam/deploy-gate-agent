"""The `deploy-gate-agent` command, built on theodosia's build_cli."""

from __future__ import annotations

from theodosia.cli import build_cli, run

from deploy_gate_agent.app import build_application

cli = build_cli(
    "deploy-gate-agent",
    application=build_application,
    help="Change/deploy gate: a Burr state machine served over MCP.",
    server_name="deploy-gate-agent",
    # run_checks reads CHANGELOG.md through this filesystem MCP server. The
    # agent only ever sees this server's `step` tool, not the filesystem tools.
    upstream={
        "fs": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]}
    },
)


def main() -> int:
    return run(cli)
