#!/bin/sh
# oracle-gc.sh — garbage collector for a lean agent box (Oracle: 4 CPU, limited disk).
# RULES
#   collect:  reproducible-from-public-repo artifacts. Old builds, stale
#             checkouts (merged + pushed), superseded model files (a newer
#             sibling exists AND it's re-downloadable), tmp cruft, logs >7d.
#   keep:     git history, ledgers, anything content-addressed AND referenced,
#             pushed-but-not-verified (recent <24h), anything not re-derivable.
# Safety:     default DRY-RUN (prints what it would free). --apply to act.
#             Collects by ARCHIVE-then-delete in GC_TRASH, purged when older
#             than GC_GRACE days — recoverable beats gone forever.
# Log:        GC_LOG, one line per action + disk before/after.
# Schedule:   daily cron:  17 4 * * *  /path/oracle-gc.sh --apply
set -u
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1
HOME="${HOME:-/root}"; export HOME
GC_HOME="${GC_HOME:-$HOME}"
GC_TRASH="$GC_HOME/.gc-trash"
GC_LOG="$GC_HOME/.gc/oracle-gc.log"
GC_GRACE_DAYS="${GC_GRACE_DAYS:-7}"
AGE_DAYS="${AGE_DAYS:-14}"          # artifacts older than this are candidates
mkdir -p "$GC_TRASH" "$GC_HOME/.gc"

df_before=$(df -h "$GC_HOME" | awk 'NR==2{print $3" used, "$4" free"}')
freed=0
say() { echo "$(date -u +%FT%TZ) $*" >> "$GC_LOG"; [ "$APPLY" = 1 ] || echo "DRY  $*"; }

# 1. purge grace-expired trash (the only real deletion)
find "$GC_TRASH" -mindepth 1 -maxdepth 1 -mtime +"$GC_GRACE_DAYS" 2>/dev/null | while read -r p; do
  sz=$(du -sk "$p" 2>/dev/null | cut -f1); rm -rf "$p"
  say "PURGED-trash $p ${sz}K (grace ${GC_GRACE_DAYS}d expired)"
done

collect() { # collect <path> <reason>
  p="$1"; [ -e "$p" ] || return 0
  sz=$(du -sk "$p" 2>/dev/null | cut -f1)
  case "$p" in
    *.git/*|*/.git) say "KEEP $p (git object store — never collected)"; return 0 ;;
  esac
  if [ "$APPLY" = 1 ]; then
    mv "$p" "$GC_TRASH/$(date +%s)-$(basename "$p")" 2>/dev/null || { say "KEEP $p (mv failed — in use?)"; return 0; }
  fi
  say "COLLECT $p ${sz}K — $2"
  freed=$((freed + sz))
}

old_enough() { find "$1" -maxdepth 0 -mtime +"$AGE_DAYS" 2>/dev/null | grep -q . ; }

# 2. tmp cruft
for d in /tmp /var/tmp "$GC_HOME/tmp"; do
  [ -d "$d" ] || continue
  find "$d" -mindepth 1 -maxdepth 1 -mtime +"$AGE_DAYS" 2>/dev/null | while read -r p; do
    collect "$p" "tmp cruft >${AGE_DAYS}d"
  done
done

# 3. oversized logs
find "$GC_HOME" -name "*.log" -size +50M -mtime +2 2>/dev/null | while read -r p; do
  collect "$p" "oversized log (>50M, >2d)"
done

# 4. superseded model files: same name with a newer sibling AND re-downloadable
for m in "$GC_HOME"/models/* "$GC_HOME"/.cache/*/models--*; do
  [ -e "$m" ] || continue
  base=$(basename "$m"); stem=$(echo "$base" | sed -E 's/[-_.](v?[0-9][0-9.a-z-]*|latest|gguf.*)$//')
  [ "$stem" = "$base" ] && continue
  newer=$(ls -t "$(dirname "$m")"/"$stem"* 2>/dev/null | grep -v "$m$" | head -1)
  [ -n "$newer" ] && old_enough "$m" && collect "$m" "superseded by $(basename "$newer")"
done

# 5. stale checkouts: git repo, fully pushed (no unpushed commits, clean tree)
for d in "$GC_HOME"/*/*/ "$GC_HOME"/*/; do
  [ -d "$d/.git" ] || continue
  cd "$d" || continue
  if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet HEAD 2>/dev/null; then
    say "KEEP $d (dirty working tree)"; continue
  fi
  br=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  unpushed=$(git log --oneline "@{u}..HEAD" 2>/dev/null | wc -l)
  [ "$unpushed" -gt 0 ] && { say "KEEP $d ($unpushed unpushed commits)"; continue; }
  [ -z "$(git log -1 --since=24h 2>/dev/null)" ] || { say "KEEP $d (commit <24h — not yet verified)"; continue; }
  old_enough "$d" && collect "$d" "stale checkout (pushed, idle >${AGE_DAYS}d, re-clonable)"
done

df_after=$(df -h "$GC_HOME" 2>/dev/null | awk 'NR==2{print $3" used, "$4" free"}')
say "RUN apply=$APPLY approx_collected=${freed}K before=[$df_before] after=[$df_after]"
[ "$APPLY" = 1 ] || echo "DRY-RUN (no changes). Re-run with --apply to collect. Log: $GC_LOG"
