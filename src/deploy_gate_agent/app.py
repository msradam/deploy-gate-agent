"""A change/deploy gate as a Burr state machine.

Shape::

    open_change --> run_checks (loop) --> approve --> deploy --> verify --> resolve
                                                                       \\-> rollback

Two kinds of gate, both demonstrated:

* Structural gates (the transition graph). There is no edge that lets the
  agent ``deploy`` before ``approve``, or ``approve`` before ``run_checks``.
  Out-of-order calls come back as ``invalid_transition``.
* A body-level gate. ``resolve`` raises if the post-deploy health check did
  not pass, so a green "close it out" only happens on a healthy deploy; the
  unhealthy path is ``rollback``.

Every transition is recorded to Burr's tracker, so the change has an audit
trail: who approved, what was deployed, whether it verified, and how it ended.
Theodosia also hash-chains each step and refusal into a tamper-evident ledger
next to the tracker log, checkable with ``deploy-gate-agent verify``.
"""

from __future__ import annotations

from burr.core import ApplicationBuilder, State, action
from burr.core.action import Condition
from theodosia import tracker

from theodosia import call_upstream


@action(reads=[], writes=["stage", "service", "summary"])
def open_change(state: State, service: str, summary: str) -> State:
    """Open a change request.

    Args:
        service: The service being changed, e.g. "checkout-api".
        summary: One-line description of the change.
    """
    return state.update(stage="open", service=service, summary=summary)


@action(reads=[], writes=["stage", "checks", "change_documented"])
async def run_checks(state: State) -> State:
    """Run pre-deploy checks, and confirm the change is documented.

    The documentation check reads CHANGELOG.md from a separate filesystem MCP
    server through `call_upstream`. The graph reaches into another MCP server
    from inside an action; the agent never sees that server's tools.
    """
    checks = {"lint": "pass", "tests": "pass", "security": "pass"}
    try:
        changelog = await call_upstream("fs", "read_file", {"path": "CHANGELOG.md"})
        change_documented = bool(changelog)
    except Exception:
        change_documented = False
    return state.update(stage="checked", checks=checks, change_documented=change_documented)


@action(reads=["checks"], writes=["stage", "approver"])
def approve(state: State, approver: str) -> State:
    """Record sign-off. Reachable only after checks have run.

    Args:
        approver: Who approved the change.
    """
    return state.update(stage="approved", approver=approver)


@action(reads=["service", "approver"], writes=["stage", "deployed_version"])
def deploy(state: State, version: str) -> State:
    """Deploy. Reachable only after approval.

    Args:
        version: The version/tag being deployed.
    """
    return state.update(stage="deployed", deployed_version=version)


@action(reads=["service"], writes=["stage", "healthy"])
def verify(state: State, healthy: bool) -> State:
    """Record the post-deploy health check.

    Args:
        healthy: Whether the deploy passed its health check.
    """
    return state.update(stage="verified", healthy=healthy)


@action(reads=["healthy", "deployed_version"], writes=["stage", "outcome"])
def resolve(state: State, notes: str = "") -> State:
    """Close out a healthy deploy. Refuses if the health check failed.

    Args:
        notes: Optional closing notes.
    """
    if not state["healthy"]:
        raise ValueError("cannot resolve: health check did not pass; rollback instead")
    return state.update(stage="resolved", outcome=f"deployed {state['deployed_version']}; {notes}")


@action(reads=["service", "deployed_version"], writes=["stage", "outcome"])
def rollback(state: State, reason: str) -> State:
    """Revert the deploy. The unhealthy path.

    Args:
        reason: Why the change is being rolled back.
    """
    return state.update(stage="rolled_back", outcome=f"rolled back {state['service']}: {reason}")


def build_application():
    """Build the deploy-gate Burr Application."""
    is_open = Condition.expr("stage == 'open'")
    checked = Condition.expr("stage == 'checked'")
    approved = Condition.expr("stage == 'approved'")
    deployed = Condition.expr("stage == 'deployed'")
    verified = Condition.expr("stage == 'verified'")
    return (
        ApplicationBuilder()
        .with_actions(
            open_change=open_change,
            run_checks=run_checks,
            approve=approve,
            deploy=deploy,
            verify=verify,
            resolve=resolve,
            rollback=rollback,
        )
        .with_transitions(
            ("open_change", "run_checks", is_open),
            ("run_checks", "run_checks", checked),
            ("run_checks", "approve", checked),
            ("approve", "deploy", approved),
            ("deploy", "verify", deployed),
            ("verify", "resolve", verified),
            ("verify", "rollback", verified),
        )
        .with_tracker(tracker(project="deploy-gate-agent"))
        .with_state(stage="new")
        .with_entrypoint("open_change")
        .build()
    )
