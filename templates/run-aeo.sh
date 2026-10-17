#!/bin/sh
# Runs the AEO agent unattended for every site under AEO_ROOT. Usage: run-aeo.sh daily|weekly
# Written by /aeo-agent:aeo setup. Edit ALLOWED if you add or remove connectors.
set -eu
MODE="${1:-weekly}"
ROOT="${AEO_ROOT:-$HOME/Documents/AEO}"
ALLOWED="__ALLOWED_TOOLS__"
mkdir -p "$ROOT/logs"
cd "$ROOT"
claude -p "/aeo-agent:aeo --all $MODE --scheduled" \
  --permission-mode acceptEdits \
  --allowedTools "$ALLOWED" \
  >> "$ROOT/logs/$MODE-$(date +%Y-%m-%d).log" 2>&1
