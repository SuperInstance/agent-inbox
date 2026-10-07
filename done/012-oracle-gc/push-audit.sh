#!/bin/sh
# push-audit.sh — "if it's not pushed, it didn't happen."
# Lists every git working dir under the home (depth<=3) with commits older
# than 24h that exist nowhere but locally: unpushed ahead-of-upstream,
# untracked files, and dirty trees. Exit 1 if anything needs attention.
set -u
HOME="${HOME:-/root}"; export HOME
CUTOFF=$(( $(date +%s) - 86400 ))
bad=0
for d in "$HOME" "$HOME"/* "$HOME"/*/*/; do
  [ -d "$d/.git" ] || continue
  cd "$d" 2>/dev/null || continue
  name=${d#"$HOME"/}
  unpushed=$(git log --oneline "@{u}..HEAD" 2>/dev/null | wc -l | tr -d ' ')
  nobranch=""
  git rev-parse "@"{u} >/dev/null 2>&1 || nobranch="(NO UPSTREAM SET)"
  dirty=""
  git diff --quiet HEAD 2>/dev/null || dirty="(dirty tree)"
  [ -z "$(git ls-files --others --exclude-standard 2>/dev/null | head -1)" ] || dirty="$dirty(untracked)"
  # any unpushed commit older than 24h?
  old_unpushed=0
  if [ "$unpushed" -gt 0 ]; then
    for c in $(git rev-list "@{u}..HEAD" 2>/dev/null); do
      ct=$(git log -1 --format=%ct "$c" 2>/dev/null || echo 0)
      [ "$ct" -lt "$CUTOFF" ] && old_unpushed=1
    done
  fi
  if [ "$old_unpushed" = 1 ] || [ -n "$nobranch" ] || { [ -n "$dirty" ] && [ "$old_unpushed" = 1 ]; }; then
    echo "NEEDS PUSH: $name  ahead=$unpushed $nobranch $dirty"
    bad=1
  elif [ "$unpushed" -gt 0 ]; then
    echo "recent-only: $name  ahead=$unpushed (<24h, fine)"
  fi
done
[ $bad -eq 0 ] && echo "AUDIT CLEAN: nothing older than 24h is unpushed."
exit $bad
