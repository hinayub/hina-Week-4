#!/usr/bin/env bash
# Project-scoped PreToolUse hook: append a timestamped line for every tool call.
# Reads the hook payload (JSON) from stdin; no jq dependency.
# Logs into this project's .claude/ dir (derived from the script's own path).
here="$(cd "$(dirname "$0")" && pwd)"
log_file="$here/../tool-calls.log"   # -> <project>/.claude/tool-calls.log
input=$(cat)
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
tool=$(printf '%s' "$input" \
  | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 \
  | sed -E 's/.*"([^"]*)"$/\1/')
[ -z "$tool" ] && tool="unknown"
printf '%s\t%s\n' "$ts" "$tool" >> "$log_file"
exit 0
