"""Seed one deploy-gate-agent session for the demo recording.

Walks an unhealthy deploy so the timeline shows the body-level gate: `resolve`
refuses on a failed health check (red row), and the run ends in `rollback`.
Runs without an upstream binding, so `run_checks` records
`change_documented=False` and still advances.
"""

from __future__ import annotations

import asyncio

from fastmcp import Client

from burrmcp import ServingMode, mount
from deploy_gate_agent.app import build_application


async def main() -> None:
    server = mount(build_application(), mode=ServingMode.STEP, name="deploy-gate-agent")
    async with Client(server) as client:

        async def step(action, **inputs):
            await client.call_tool("step", {"action": action, "inputs": inputs})

        await step("open_change", service="checkout-api", summary="bump to v2.4.0")
        await step("run_checks")
        await step("approve", approver="alice")
        await step("deploy", version="v2.4.0")
        await step("verify", healthy=False)
        await step("resolve")  # refusal: health check failed (action_error)
        await step("rollback", reason="health check failed after deploy")


if __name__ == "__main__":
    asyncio.run(main())
