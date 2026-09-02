#!/bin/bash
# SessionStart: tell the session where the learner left off.
# Read-only. Always exits 0 and always emits valid JSON or nothing — a broken
# greeting must never break a session.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
[ -d "$ROOT/topics" ] || exit 0

python3 - "$ROOT" <<'PY' 2>/dev/null || exit 0
import json, os, re, sys, glob

root = sys.argv[1]
lines = []
for pf in sorted(glob.glob(os.path.join(root, "topics", "*", "progress.md"))):
    slug = os.path.basename(os.path.dirname(pf))
    try:
        t = open(pf, encoding="utf-8").read()
    except OSError:
        continue

    def field(name):
        m = re.search(r"^\|\s*\*\*" + re.escape(name) + r"\*\*\s*\|\s*(.*?)\s*\|", t, re.M)
        return m.group(1).strip() if m else "—"

    shaky = re.findall(r"^\|\s*([^|]+?)\s*\|[^|]*\|\s*`shaky`", t, re.M)
    carry = [l.strip()[6:].strip() for l in t.splitlines() if l.strip().startswith("- [ ]")]

    lines.append(f"- **{slug}** — {field('Modules complete')} complete · next: {field('Next module')} · last session: {field('Last session')}")
    if shaky:
        lines.append(f"  - shaky ({len(shaky)}): " + "; ".join(s.strip() for s in shaky[:4]))
    if carry:
        lines.append(f"  - queued: {carry[0]}" + (f" (+{len(carry)-1} more)" if len(carry) > 1 else ""))

if not lines:
    sys.exit(0)

ctx = ("Learning state in this repo (from each topic's progress.md):\n"
       + "\n".join(lines)
       + "\n\nCommands: /teach to continue · /review for a short drill · /progress for status "
         "· /learn <concept> to build a new topic. Do not write to any progress.md outside a "
         "/teach or /review session.")

print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": ctx}}))
PY
