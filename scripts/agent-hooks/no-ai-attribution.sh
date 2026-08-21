#!/usr/bin/env sh
# PreToolUse hook for local commit-message guardrails.
# Reads the hook JSON from stdin; if the pending Bash command is a `git commit`
# carrying tool attribution, blocks it (exit 2) with a reason on stderr.
PAYLOAD="$(cat)"
printf '%s' "$PAYLOAD" | grep -q 'git commit' || exit 0
if printf '%s' "$PAYLOAD" | grep -Eiq 'co-authored-by:|generated (with|by)|written (with|by)|🤖'; then
  echo "Blocked: commit message contains tool attribution. Project rule (AGENTS.md): no tool attribution in commits/comments/PRs. Rewrite the message without it." >&2
  exit 2
fi
exit 0
