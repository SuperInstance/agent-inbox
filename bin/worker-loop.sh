#!/bin/bash
# worker-loop.sh — unattended claim→work→done loop.
# Usage: worker-loop.sh --id <worker-id> --work-cmd "<cmd>" [--interval 60]
# The work command is called as: <cmd> <taskfile> <resultdir>
# and must exit 0 on success. Results are collected from <resultdir>.
set -euo pipefail

ID=""; WORK_CMD=""; INTERVAL=60
while [ $# -gt 0 ]; do
  case "$1" in
    --id) ID="$2"; shift 2 ;;
    --work-cmd) WORK_CMD="$2"; shift 2 ;;
    --interval) INTERVAL="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done
[ -n "$ID" ] || { echo "--id required" >&2; exit 1; }
[ -n "$WORK_CMD" ] || { echo "--work-cmd required" >&2; exit 1; }

REPO_DIR="${AGENT_INBOX_DIR:-$HOME/agent-inbox}"
[ -d "$REPO_DIR/.git" ] || { echo "no repo at $REPO_DIR" >&2; exit 1; }
export PATH="$REPO_DIR/bin:$PATH"

echo "worker-loop: id=$ID interval=${INTERVAL}s"
while true; do
  git -C "$REPO_DIR" pull --quiet 2>/dev/null || true
  task=""
  for f in "$REPO_DIR"/inbox/*.md; do
    [ -e "$f" ] || continue
    task="$(basename "$f")"
    # honor `to:` addressing — skip tasks reserved for another worker
    # (unless unclaimed >24h; keep it simple: check the to: line)
    to_line="$(grep -m1 '^to:' "$f" | awk '{print $2}')"
    if [ -n "$to_line" ] && [ "$to_line" != "any" ] && [ "$to_line" != "$ID" ]; then
      age_h=$(( ($(date +%s) - $(git -C "$REPO_DIR" log -1 --format=%ct -- "inbox/$task")) / 3600 ))
      [ "$age_h" -ge 24 ] || { task=""; continue; }
    fi
    break
  done

  if [ -n "$task" ]; then
    echo "claiming: $task"
    if inbox claim "$task" "$ID" 2>/dev/null; then
      rdir="$(mktemp -d)"
      set +e
      bash -c "$WORK_CMD \"$REPO_DIR/claimed/$ID/$task\" \"$rdir\""
      rc=$?
      set -e
      if [ "$rc" -eq 0 ]; then
        [ -f "$rdir/result.md" ] || echo -e "**DONE**\n\n(no result.md written by work command)" > "$rdir/result.md"
        inbox done "$task" "$ID" "$rdir"/*
      else
        echo "work command failed (rc=$rc) for $task — releasing"
        git -C "$REPO_DIR" mv "claimed/$ID/$task" "inbox/$task"
        git -C "$REPO_DIR" commit -qm "release: $task by $ID (work failed rc=$rc)"
        git -C "$REPO_DIR" push --quiet 2>/dev/null || true
      fi
      rm -rf "$rdir"
    else
      echo "claim raced, will retry next tick"
    fi
  fi
  sleep "$INTERVAL"
done
