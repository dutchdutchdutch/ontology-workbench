#!/usr/bin/env bash
# Print a project's step status by scanning which files exist. Nothing is stored; this is the
# generated index. The table in CLAUDE.md "How to tell status" is the specification.
# Usage, from the workspace root:  tools/status.sh <name>
set -eu
cd "$(dirname "$0")/.."

name="${1:-}"
if [ -z "$name" ]; then
  echo "usage: tools/status.sh <name>" >&2
  exit 2
fi
p="projects/$name"
if [ ! -d "$p" ]; then
  echo "no such project: $p" >&2
  exit 1
fi

row() { printf '| %-11s | %-50s | %s\n' "$1" "$2" "$3"; }
next=""

echo "Project: $name   ($p)"
echo
printf '| %-11s | %-50s | %s\n' "Step" "State" "Then"
printf '|-%-11s-|-%-50s-|-%s\n' "-----------" "--------------------------------------------------" "----"

# 00 sources
if [ -f "$p/00-sources/manifest.md" ]; then
  # rows under "## Not pulled", not counting the table header and its separator line
  notpulled=$(awk '/^## Not pulled/{f=1;next} f&&/^## /{f=0} f&&/^\|/{c++} END{print (c>2?c-2:0)}' "$p/00-sources/manifest.md")
  if [ "$notpulled" -gt 0 ]; then
    row "00 sources" "manifest.md, $notpulled source(s) not pulled" "fix access, re-run 00"
  else
    row "00 sources" "manifest.md" "run 01"
  fi
  [ -z "$next" ] && next="run step 01 (factory/steps/01-terms/CONTEXT.md)"
else
  row "00 sources" "not run" "run 00"
  next="run step 00 (factory/steps/00-sources/CONTEXT.md)"
fi

# 01 terms
inv=$(ls "$p"/01-terms/inventory-*.md 2>/dev/null | wc -l | tr -d " " || true)
review="$p/01-terms/review.md"
if [ "$inv" -gt 0 ]; then
  names=$(ls "$p"/01-terms/inventory-*.md | sed 's#.*/inventory-##; s#\.md##' | tr '\n' ' ' | sed 's/ $//')
  ext=$(grep -l '^produced_by: external' "$p"/01-terms/inventory-*.md 2>/dev/null | wc -l | tr -d " " || true)
  state="$inv inventor$( [ "$inv" -eq 1 ] && echo y || echo ies ): $names"
  [ "$ext" -gt 0 ] && state="$state ($ext external)"
  if [ -f "$review" ]; then
    # a review row whose third cell is "missing"
    missing=$(grep -c '^|[^|]*|[^|]*| *missing *|' "$review" || true)
    # signed when `reviewed:` holds a date. `none`, empty or the <YYYY-MM-DD> placeholder is not
    signed=$(grep -m1 '^reviewed:' "$review" | sed 's/^reviewed: *//; s/ *#.*//; s/ *$//')
    case "$signed" in [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;; *) signed="" ;; esac
    if [ "$missing" -gt 0 ]; then
      row "01 terms" "$state, review.md: $missing missing" "re-run 01 with the review"
      next="re-run step 01 with $review ($missing term(s) marked missing)"
    elif [ -z "$signed" ]; then
      row "01 terms" "$state, review.md unsigned" "read the inventories, sign review.md"
      next="read each inventory, then sign $review: fill reviewed: with today's date"
    else
      row "01 terms" "$state, review.md signed $signed" "run 02"
      next="run step 02 (factory/steps/02-delta/CONTEXT.md)"
    fi
  else
    row "01 terms" "$state, no review.md" "write 01-terms/review.md"
    next="write $review, the gate for step 02 (factory/steps/01-terms/CONTEXT.md)"
  fi
else
  row "01 terms" "no inventory" "run 01"
fi

# 02 delta
if [ -f "$p/02-delta/delta-report.md" ]; then
  row "02 delta" "delta-report.md" "run 03"
  next="run step 03 (factory/steps/03-merge/CONTEXT.md)"
elif [ -f "$p/02-delta/skipped.md" ]; then
  reason=$(grep -m1 '^reason:' "$p/02-delta/skipped.md" | sed 's/^reason: *//')
  row "02 delta" "skipped: $reason" "run 03"
  next="run step 03 (factory/steps/03-merge/CONTEXT.md)"
else
  row "02 delta" "not run" "$( [ -f "$review" ] && echo 'run 02' || echo 'needs 01-terms/review.md first')"
fi
[ -f "$p/02-delta/drift-report.md" ] && row "" "drift-report.md present" "read it"

# 03 merge
if [ -f "$p/03-merge/inventory-merged.md" ]; then
  row "03 merge" "inventory-merged.md$( [ -f "$p/03-merge/conflicts.md" ] && echo ', conflicts.md' )" "run 04"
  next="run step 04 (factory/steps/04-draft/CONTEXT.md)"
elif [ -f "$p/03-merge/skipped.md" ]; then
  reason=$(grep -m1 '^reason:' "$p/03-merge/skipped.md" | sed 's/^reason: *//')
  row "03 merge" "skipped: $reason" "run 04"
  next="run step 04 (factory/steps/04-draft/CONTEXT.md)"
else
  row "03 merge" "not run" "$( [ "$inv" -ge 2 ] && echo 'run 03' || echo 'needs 2+ inventories, or writes skipped.md')"
fi

# 04 draft
vmax=$(ls -d "$p"/04-draft/v[0-9]* 2>/dev/null | sed 's#.*/v##' | sort -n | tail -1)
rulings=$(ls "$p"/decisions/[0-9][0-9][0-9]-*.md 2>/dev/null | wc -l | tr -d " " || true)
if [ -n "${vmax:-}" ]; then
  if [ -f "$p/04-draft/v$vmax/blocked-by-rulings.md" ] && [ ! -f "$p/04-draft/v$vmax/glossary.md" ]; then
    row "04 draft" "v$vmax BLOCKED by a ruling" "resolve in decisions/, re-run 04"
    next="resolve $p/04-draft/v$vmax/blocked-by-rulings.md in decisions/, then re-run step 04"
  else
    state="v$vmax"
    [ "$vmax" -eq 1 ] && state="$state (unreviewed)" || state="$state (reviewed)"
    q="$p/04-draft/v$vmax/verification-queue.md"
    [ -f "$q" ] && state="$state, queue present"
    row "04 draft" "$state" "$( [ "$vmax" -ge 2 ] && echo 'run 05 if queue has no core term' || echo 'review: rulings to decisions/, re-run 04')"
    if [ "$vmax" -ge 2 ]; then next="run step 05 (factory/steps/05-glossary/CONTEXT.md) once the queue holds no core term"; else next="answer $q into $p/decisions/, then re-run step 04"; fi
  fi
else
  row "04 draft" "no draft" "run 04"
fi
row "decisions" "$rulings ruling$( [ "$rulings" -eq 1 ] || echo s)" "$( [ "$rulings" -gt 0 ] && echo 'replayed by every 04 run' || echo 'write one per expert answer')"

# 05 glossary: published, then a stage in the glossary header (review, trial, adopted)
g="$p/05-glossary/glossary.md"
fb="$p/05-glossary/feedback.md"
if [ -f "$g" ]; then
  stage=$(grep -m1 '^stage:' "$g" | sed 's/^stage: *//; s/ *#.*//; s/ *$//')
  from=$(grep -m1 '^published_from:' "$g" | sed 's/^published_from: *//; s/ *#.*//; s/ *$//')
  base="published${from:+ from $from}"
  case "${stage:-}" in
    review)
      row "05 glossary" "$base, stage review" "reviewers sign off, then stage: trial"
      next="review: reviewers sign off in $g, swap test on the core, then set stage: trial" ;;
    trial)
      if [ -f "$fb" ]; then
        # table rows after the header, whose disposition cell (the fifth) is empty
        open=$(awk -F'|' '/^\|/ && !/^\|[-: |]*$/ {n++; if (n>1 && $6 ~ /^ *$/) o++} END{print o+0}' "$fb")
        row "05 glossary" "$base, stage trial, $open open feedback" "close feedback, then stage: adopted"
        next="trial: give every open row in $fb a disposition, then set stage: adopted"
      else
        row "05 glossary" "$base, stage trial, no feedback.md" "start 05-glossary/feedback.md"
        next="trial: copy _feedback.template.md to $fb and collect feedback"
      fi ;;
    adopted)
      row "05 glossary" "$base, adopted" "02 in drift mode on a schedule; 06 on request"
      next="adopted. Run step 02 in drift mode on a schedule, step 06 on request" ;;
    *)
      row "05 glossary" "$base, no stage field" "add stage: review to the header"
      next="add stage: review to the header of $g (factory/steps/05-glossary/CONTEXT.md)" ;;
  esac
else
  row "05 glossary" "not published" "needs a v2+ draft"
fi

# 06 ontology
if [ -f "$p/06-ontology/ontology.html" ]; then
  stale=""
  if [ ! -f "$p/05-glossary/glossary.md" ]; then
    stale=" (no 05 glossary: not generated from one)"
  elif [ "$p/05-glossary/glossary.md" -nt "$p/06-ontology/ontology.html" ]; then
    stale=" (older than glossary.md: regenerate)"
  fi
  row "06 ontology" "ontology.html$stale" "open it"
elif [ -f "$p/06-ontology/skipped.md" ]; then
  reason=$(grep -m1 '^reason:' "$p/06-ontology/skipped.md" | sed 's/^reason: *//')
  row "06 ontology" "skipped: $reason" "tools/render-ontology.py $name when wanted"
else
  row "06 ontology" "not rendered" "tools/render-ontology.py $name"
fi

# 07 streams: optional. Two kinds of authored file share the folder: a value stream, and a
# process (front matter holds `process:`). Each kind has its own generated page.
s="$p/07-streams"
authored=$(ls "$s"/*.md 2>/dev/null | grep -v '/_' | grep -v '/README.md$' | grep -v '/skipped.md$' || true)
streams=""; procs=""
for f in $authored; do
  if awk 'NR==1&&$0!="---"{exit 1} NR>1&&/^---/{exit 0} /^process:/{found=1} END{exit found?0:1}' "$f" 2>/dev/null; then procs="$procs $f"; else streams="$streams $f"; fi
done
unsigned_of() { local n=0 f d; for f in "$@"; do d=$(grep -m1 '^reviewed:' "$f" | sed 's/^reviewed: *//; s/ *#.*//; s/ *$//' || true); case "$d" in [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;; *) n=$((n+1)) ;; esac; done; echo $n; }
stale_of() { local page="$1"; shift; local f; for f in "$@"; do [ -f "$f" ] && [ "$f" -nt "$page" ] && { echo " (older than its inputs: regenerate)"; return; }; done; echo ""; }
if [ -n "$streams" ] || [ -n "$procs" ]; then
  if [ -n "$streams" ]; then
    n=$(echo $streams | wc -w | tr -d " "); u=$(unsigned_of $streams)
    state="$n stream file(s)"; [ "$u" -gt 0 ] && state="$state, $u unsigned"
    if [ -f "$s/value-streams.html" ]; then
      row "07 streams" "value-streams.html, $state$(stale_of "$s/value-streams.html" $streams "$p/06-ontology/ontology-data.js")" "$( [ "$u" -gt 0 ] && echo 'reviewer signs each stream file' || echo 'open it')"
    else
      row "07 streams" "$state, not rendered" "tools/render-streams.py $name"
    fi
  fi
  if [ -n "$procs" ]; then
    n=$(echo $procs | wc -w | tr -d " "); u=$(unsigned_of $procs)
    state="$n process file(s)"; [ "$u" -gt 0 ] && state="$state, $u unsigned"
    if [ -f "$s/processes.html" ]; then
      row "07 process" "processes.html, $state$(stale_of "$s/processes.html" $procs "$p/05-glossary/glossary.md")" "$( [ "$u" -gt 0 ] && echo 'reviewer signs each process file' || echo 'open it')"
    else
      row "07 process" "$state, not rendered" "tools/render-processes.py $name"
    fi
  fi
elif [ -f "$s/skipped.md" ]; then
  reason=$(grep -m1 '^reason:' "$s/skipped.md" | sed 's/^reason: *//')
  row "07 streams" "skipped: $reason" "write a stream or process file when wanted"
else
  row "07 streams" "no stream or process file (optional)" "copy a 07-streams/_*.template.md when wanted"
fi

# 08 publish: the log says what is staged and what is out, per destination
log="$p/08-publish/publish-log.md"
if [ -f "$log" ]; then
  # the latest row per destination (sixth cell): its sent cell (third) and its source version (fourth)
  summary=$(awk -F'|' '/^\| [0-9]/ {gsub(/ /,"",$6); gsub(/ /,"",$4); gsub(/ /,"",$5); last[$7]=$4" "$5} END{for (d in last) print last[d]}' "$log")
  dests=$(echo "$summary" | grep -c . || true)
  waiting=$(echo "$summary" | awk '$1=="" || $1 !~ /^[0-9]/' | grep -c . || true)
  behind=0
  if [ -n "${from:-}" ]; then
    behind=$(echo "$summary" | awk -v f="$from" '$1 ~ /^[0-9]/ && $2!=f' | grep -c . || true)
  fi
  if [ "$waiting" -gt 0 ]; then
    row "08 publish" "$dests destination(s), $waiting staged not sent" "send the outbox, then --sent"
    next="send $p/08-publish/outbox/ to each staged destination, then tools/stage-publish.py $name --sent <destination> \"<receipt>\""
  elif [ "$behind" -gt 0 ]; then
    row "08 publish" "$dests destination(s), $behind behind $from" "stage again once trial"
  else
    row "08 publish" "$dests destination(s), all sent${from:+ from $from}" "--verify on a schedule"
  fi
elif grep -q '^publish:' "$p/project.yaml" 2>/dev/null; then
  row "08 publish" "not staged" "tools/stage-publish.py $name, at trial or adopted"
else
  row "08 publish" "no publish: block in project.yaml" "name the destinations when ready"
fi

echo
echo "Next: $next"
