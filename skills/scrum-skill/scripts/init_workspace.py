#!/usr/bin/env python3
"""Initialize local Scrum records without replacing existing project work.

Python 3.10+; stdlib only. No network, Git, hooks or package installation.
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
from datetime import date, timedelta
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
VERSION = json.loads((SKILL / "assets/version.json").read_text(encoding="utf-8"))["version"]
START = "<!-- scrum-skill:begin -->"
END = "<!-- scrum-skill:end -->"
POINTER = f"""{START}
## Scrum workspace
Read `.scrum/MASTER_PROMPT.md` and `.scrum/handoffs/LATEST.md` to resume.
Keep `.scrum/` local unless the project owner explicitly chooses publication.
Apply existing project instructions first; do not infer human approval from agent notes.
{END}
"""


def specialists(value: str) -> list[str]:
    if value == "none":
        return []
    names = [part.strip() for part in value.split(",")]
    if not names or any(not re.fullmatch(r"[a-z][a-z0-9-]{0,47}", n) for n in names):
        raise ValueError("specialists must be comma-separated lowercase role slugs, or none")
    if len(set(names)) != len(names):
        raise ValueError("duplicate specialist names")
    return names


def ensure_inside(root: Path, path: Path) -> None:
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"destination escapes project root: {path}")
    current = path
    while current != root:
        if current.is_symlink():
            raise ValueError(f"symlink destination not supported: {current}")
        current = current.parent


def append_block(existing: str, block: str) -> str:
    has_start, has_end = START in existing, END in existing
    if has_start != has_end or existing.count(START) > 1 or existing.count(END) > 1:
        raise ValueError("malformed or duplicate scrum-skill pointer block")
    if has_start:
        if existing.index(START) > existing.index(END):
            raise ValueError("reversed scrum-skill pointer markers")
        return existing
    separator = "\n" if not existing or existing.endswith("\n") else "\n\n"
    return existing + separator + block


def plan(root: Path, name: str, goal: str, roles: list[str], start: date,
         sprint_days: int) -> dict[Path, str]:
    """Preflight every destination, then return only necessary writes."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("project root must be an existing directory")
    if not name.strip() or not goal.strip():
        raise ValueError("project name and goal must be non-empty")
    if not 1 <= sprint_days <= 31:
        raise ValueError("sprint-days must be between 1 and 31")
    state_dir = root / ".scrum"
    ensure_inside(root, state_dir)
    manifest = state_dir / "workspace.json"
    if manifest.exists():
        ensure_inside(root, manifest)
        prior = json.loads(manifest.read_text(encoding="utf-8"))
        if prior.get("project_name") != name:
            raise ValueError("existing Scrum workspace belongs to a different project name")
        # Resumption preserves the existing Goal, roles, dates, version and decisions.
        try:
            goal = prior["product_goal"]
            roles = specialists(",".join(prior["specialists"])) if prior["specialists"] else []
            start = date.fromisoformat(prior["forecast_start"])
            sprint_days = prior["sprint_days"]
            if not isinstance(goal, str) or not goal.strip() or not isinstance(sprint_days, int):
                raise ValueError("invalid existing workspace metadata")
        except (KeyError, TypeError) as error:
            raise ValueError("invalid existing workspace metadata") from error
    if not 1 <= sprint_days <= 31:
        raise ValueError("sprint-days must be between 1 and 31")
    next_month, next_year = (start.month % 12) + 1, start.year + (start.month == 12)
    limit = date(next_year, next_month,
                 min(start.day, calendar.monthrange(next_year, next_month)[1]))
    if start + timedelta(days=sprint_days) > limit:
        raise ValueError("chosen Sprint would exceed one calendar month")
    end = start + timedelta(days=sprint_days - 1)

    state = {"skill_version": VERSION, "project_name": name, "product_goal": goal,
             "product_owner": "human user (confirm identity if needed)",
             "specialists": roles, "sprint_days": sprint_days,
             "forecast_start": start.isoformat(), "forecast_end": end.isoformat(),
             "state": "proposed", "authorization": "setup only; use actual user instructions"}
    team = "\n".join(f"- {role}: adaptable specialist profile in roles/{role}.md" for role in roles)
    artifacts = {
        "workspace.json": json.dumps(state, indent=2) + "\n",
        "PRODUCT_GOAL.md": f"# Product Goal\n\n{goal}\n\nState: user-supplied direction; scope/refinement pending.\n",
        "TEAM.md": "# Team agreement\n\nHuman Product Owner: accountable for value and backlog ordering.\n"
                   "Scrum Master assistance: facilitate, inspect evidence and remove impediments.\n"
                   "Developers: one cross-functional team owns its delivery plan and estimates.\n\n"
                   + (team or "- Sequential generalist mode; no spawned agents claimed.") +
                   "\n\nProfile selection is configurable; no legal qualification or vendor tool is required.\n",
        "PRODUCT_BACKLOG.md": "# Ordered Product Backlog\n\nState: refinement pending; no accepted items or estimates invented.\n\n"
                              "| Order | ID | User outcome | Confirmation | Estimate/uncertainty | Evidence | State |\n"
                              "| --- | --- | --- | --- | --- | --- | --- |\n",
        "DEFINITION_OF_DONE.md": "# Shared Definition of Done\n\nState: proposed; tailor to product and organization standards.\n\n"
                                 "- Observable acceptance outcomes and usable integrated behavior.\n"
                                 "- Applicable project tests/checks and required reviews evidenced at exact revision.\n"
                                 "- Documentation, recoverability and handoff appropriate to scope.\n"
                                 "- Unavailable checks and unresolved quality requirements remain unfinished.\n\n"
                                 "Source merge, stakeholder acceptance, deployment and release are separate states.\n",
        "DECISIONS.md": "# Decisions\n\n| ID | Question | Accountable person | Actual decision/source/date | Status |\n"
                        "| --- | --- | --- | --- | --- |\n",
        "IMPEDIMENTS.md": "# Impediments\n\n| ID | Observed obstacle | Goal impact | Owner | Next action | Status |\n"
                          "| --- | --- | --- | --- | --- | --- |\n",
        "EVIDENCE.md": "# Evidence map\n\n| Item/criterion | Required evidence | Revision/environment | Observed result | Limitation |\n"
                       "| --- | --- | --- | --- | --- |\n",
        "sprints/SPRINT-01.md": f"# Sprint 1 forecast\n\nForecast: {start} to {end}; not an agreed planning event.\n"
                                "Sprint Goal: proposed during refinement; none accepted yet.\n"
                                "Selected items and Developers' plan: pending.\n\n"
                                "Record why, what, how, actual capacity and DoD before treating this as an active Sprint.\n",
        "sprints/SPRINT-01-PLANNING.md": "# Sprint Planning preparation\n\nState: preparation only; no attendees or agreement invented.\n"
                                         "Record Product/Sprint Goal, selected outcomes, delivery plan, forecasts/risks and actual decision evidence.\n",
        "sprints/SPRINT-01-REVIEW.md": "# Sprint Review preparation\n\nState: not held; no Done Increment or stakeholder feedback claimed.\n"
                                      "Inspect Done outcomes/quality evidence, real feedback and backlog adaptations; unfinished items return to the backlog.\n",
        "sprints/SPRINT-01-RETROSPECTIVE.md": "# Retrospective preparation\n\nState: not held.\n"
                                             "Inspect what helped/hindered, assumptions, quality/collaboration and a few owned measurable improvements.\n",
        "handoffs/INITIAL.md": "# Initialization handoff\n\nCreated local records from the user's setup inputs.\n"
                               "No implementation, tests, stakeholder ceremony, release or Git publication performed by this helper.\n\n"
                               "Next: inspect existing project instructions and refine Goal, team, backlog and DoD.\n",
        "handoffs/LATEST.md": "# Latest checkpoint\n\nWorkspace initialized; planning is proposed, no work claimed Done.\n"
                              "Read INITIAL.md, ../TEAM.md, ../PRODUCT_GOAL.md, ../PRODUCT_BACKLOG.md and ../MASTER_PROMPT.md.\n",
        "MASTER_PROMPT.md": "# Fresh-session entrypoint\n\nRead project AGENTS.md and this workspace's TEAM, Goal, backlog, DoD and handoffs/LATEST.\n"
                            "Inspect actual files/revision/evidence before resuming. Reconcile stale status rather than reinitializing.\n"
                            "Respect user/project permissions; do not infer agreement, test success or human judgment.\n"
                            "Refine the first usable slice and start it only when delivery is requested.\n",
    }
    profile = (SKILL / "assets/role-profile.md").read_text(encoding="utf-8")
    for role in roles:
        artifacts[f"roles/{role}.md"] = profile.replace("[specialism]", role)
    writes: dict[Path, str] = {}
    for rel, body in artifacts.items():
        target = state_dir / rel
        ensure_inside(root, target)
        if target.exists():
            if not target.is_file():
                raise ValueError(f"file destination is not a file: {target}")
        else:
            writes[target] = body
    for rel in ("AGENTS.md", "CLAUDE.md", ".gitignore"):
        target = root / rel
        ensure_inside(root, target)
        if target.exists() and not target.is_file():
            raise ValueError(f"file destination is not a file: {target}")
        # newline='' preserves existing text bytes, including CRLF, when appending.
        old = ""
        if target.exists():
            with target.open(encoding="utf-8", newline="") as stream:
                old = stream.read()
        block = f"{START}\n/.scrum/\n{END}\n" if rel == ".gitignore" else POINTER
        new = append_block(old, block)
        if new != old:
            writes[target] = new
    # Check parent collisions before any writes, including missing intermediate dirs.
    for target in writes:
        for parent in target.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"parent destination is not a directory: {parent}")
    return writes


def apply(writes: dict[Path, str]) -> None:
    for path, text in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            stream.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--specialists", default="engineering,qa")
    parser.add_argument("--start-date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--sprint-days", type=int, default=14)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        writes = plan(args.root, args.name, args.goal, specialists(args.specialists),
                      args.start_date, args.sprint_days)
        if not args.dry_run:
            apply(writes)
        verb = "Would write" if args.dry_run else "Wrote"
        print(f"{verb} {len(writes)} files; existing records preserved.")
        for path in writes:
            print(path.relative_to(args.root.resolve()))
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(2, f"scrum-skill: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
