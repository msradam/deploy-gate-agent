# Demo: an LLM driving deploy-gate-agent over MCP, replayed at a readable pace.
# Record with: vhs demos/deploy-gate-agent-agent.tape

Output demos/deploy-gate-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 18
Set Width 1240
Set Height 540
Set Padding 24
Set TypingSpeed 24ms

Hide
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type "python scripts/agent_demo.py"
Enter
Sleep 500ms
Show
Sleep 12s
Screenshot demos/deploy-gate-agent-agent.png
