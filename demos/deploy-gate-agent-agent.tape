# Demo: an LLM (via fast-agent) driving deploy-gate-agent over MCP, Rose Pine.
# run_checks reaches a filesystem MCP server, so this also exercises upstream.
# Record with: GOOGLE_API_KEY=... vhs demos/deploy-gate-agent-agent.tape

Output demos/deploy-gate-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 14
Set Width 1240
Set Height 800
Set Padding 20
Set TypingSpeed 24ms

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

Type `uvx fast-agent-mcp go --servers deploy-gate-agent --model generic.meta-llama/Llama-3.3-70B-Instruct-Turbo -m "Ship version v2.4.0 of checkout-api. Follow the change process end to end; the post-deploy health check passes."`
Sleep 600ms
Enter
Sleep 42s
Screenshot demos/deploy-gate-agent-agent.png
