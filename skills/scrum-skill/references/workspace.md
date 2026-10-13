# Workspace creation and resumption

For a new project, run the helper with explicit root/name/goal, after inspecting
existing instructions. It is optional; create equivalent records manually when Python
is unavailable. Use the user's language/tools and existing record layout.

```text
python <skill-directory>/scripts/init_workspace.py --root <project-directory> --name <project-name> --goal <user-outcome> --dry-run
```

Then run the same command without --dry-run when setup is authorized. Python3.10+
is needed only for the helper. It has no third-party dependencies, Git/network calls,
hooks, background agents, account creation or package installation.

It creates .scrum/ with goal/backlog, team, DoD, sprint records, evidence/decision/
impediment logs, handoffs, LATEST and master prompt. Planning is ignored by default;
AGENTS.md and CLAUDE.md get a small marked pointer block, preserving prior text.
Existing records are never overwritten. Conflicting project identity is an error,
not silent reinitialization. Symlink escapes and filesystem conflicts fail preflight.

Use --specialists engineering,qa,design for chosen profiles, or --specialists none
for a sequential generalist. The helper's default engineering,qa is an example
software team, not a Scrum requirement. --sprint-days 14 is the default calendar
forecast; choose1-31 days. The initial state is proposed, with no claimed events,
accepted Sprint Goal, measured velocity, test success or delivered Increment.

For existing projects: choose a record map rather than blindly initializing a second
board. Read current goal/DoD/backlog and latest handoffs, inspect actual branch/files
and relevant revision-specific checks, reconcile stale claims, then take the next
authorized action. Preserve previously granted permissions and user decisions.
If the helper finds existing .scrum/ state, it preserves it; updating a real Goal or
DoD requires ordinary project refinement, not a destructive bootstrap flag.

Local planning may be made public only when the user/project policy authorizes it
and content is appropriate. Do not ignore public runtime source folders, force-track
private records or assume a public repository is an instruction to publish plans.
