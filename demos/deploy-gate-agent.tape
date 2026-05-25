# Demo: deploy-gate-agent render + sessions show, Rose Pine.
# Record with: vhs demos/deploy-gate-agent.tape

Output demos/deploy-gate-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 16
Set Width 1240
Set Height 620
Set Padding 20
Set TypingSpeed 28ms

Hide
Type "export VIRTUAL_ENV_DISABLE_PROMPT=1"
Enter
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type `export PS1="(deploy-gate-agent) > "`
Enter
Type "clear"
Enter
Show

# The graph: no path to deploy before approve, or approve before checks.
Type "deploy-gate-agent render"
Sleep 600ms
Enter
Sleep 3s

Hide
Type "python scripts/seed.py >/dev/null 2>&1"
Enter
Sleep 4s
Type "clear"
Enter
Show

# The recorded change: an unhealthy deploy, resolve refused (red), rollback.
Type "deploy-gate-agent sessions show --project deploy-gate-agent"
Sleep 600ms
Enter
Sleep 2s
Screenshot demos/deploy-gate-agent.png
Sleep 2s
